#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer23_cleanup.py
  • превращает все одноэлементные кортежные импорты
        (obj,) = (importlib.import_module('pkg').obj.pkg.obj,)
    в   from pkg import obj
  • то же для 2-3-х элементов (SimpleRequestHandler, setup_application) …
  • переименовывает:
        K585qaYUbA_y -> SUB_PATH
        Di3ZYNq4y1Jk -> hook_url
        err          -> exc  (в except-блоках и логах)
  • убирает оставшиеся одноэлементные кортежи в присваиваниях
  сохраняет результат как layer23.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize, keyword

SRC = pathlib.Path("layer22.py")
DST = pathlib.Path("layer23.py")

code = SRC.read_text("utf-8")
mod  = ast.parse(code, SRC.name)

# ───────── helpers ─────────
def mod_attr(node: ast.AST) -> tuple[str, str] | None:
    """
    importlib.import_module('pkg.sub').attr(.attr)  ->  ('pkg.sub', 'attr')
    """
    if not isinstance(node, ast.Attribute):
        return None
    attr = node.attr
    val  = node.value
    # уберём дублирование .attr.attr
    if isinstance(val, ast.Attribute) and val.attr == attr:
        val = val.value
    if (isinstance(val, ast.Call) and isinstance(val.func, ast.Attribute)
            and isinstance(val.func.value, ast.Name)
            and val.func.value.id == "importlib"
            and val.func.attr == "import_module"
            and val.args and isinstance(val.args[0], ast.Constant)
            and isinstance(val.args[0].value, str)):
        return val.args[0].value, attr
    return None

imports: list[str] = []
rename: dict[str, str] = {}
new_body: list[ast.stmt] = []

for node in mod.body:
    if (isinstance(node, ast.Assign) and len(node.targets) == 1):
        tgt = node.targets[0]
        val = node.value
        # разворачиваем одноэлементные кортежи
        if isinstance(val, ast.Tuple) and len(val.elts) == 1:
            val = val.elts[0]
        # кортежная распаковка импорта
        if isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple) \
                and len(tgt.elts) == len(val.elts):
            infos = [mod_attr(e) for e in val.elts]
            pkgs  = {p for p, a in infos if p} if all(infos) else set()
            if len(pkgs) == 1:
                pkg = pkgs.pop()
                names = []
                for left, (_, attr) in zip(tgt.elts, infos):
                    if isinstance(left, ast.Name):
                        names.append(attr)
                        rename[left.id] = attr
                imports.append(f"from {pkg} import {', '.join(names)}")
                continue
        # одиночное
        if isinstance(tgt, ast.Name):
            info = mod_attr(val)
            if info:
                pkg, attr = info
                alias = attr if not keyword.iskeyword(attr) else f"{attr}_"
                imports.append(f"from {pkg} import {attr}" + (f" as {alias}" if alias != attr else ""))
                rename[tgt.id] = alias
                continue
    # не обработано — оставить
    new_body.append(node)

mod.body = new_body

# ───────── serialize AST ─────────
try:
    body_code = ast.unparse(mod)
except AttributeError:
    import astor
    body_code = astor.to_source(mod)

# ───────── доп. глобальные переименования ─────────
rename.update({
    "K585qaYUbA_y": "SUB_PATH",
    "Di3ZYNq4y1Jk": "hook_url",
    # «err» -> «exc» только если «err» не объявлен нигде
})
if "err" not in rename and "err" not in body_code:
    # ничего не делать
    pass
else:
    rename["err"] = "exc"

# токен-замена
out = []
stream = io.StringIO(body_code)
for tok in tokenize.generate_tokens(stream.readline):
    typ, string, *rest = tok
    if typ == tokenize.NAME and string in rename:
        string = rename[string]
    out.append((typ, string, *rest))

header = "\n".join(sorted(set(imports))) + "\n\n" if imports else ""
DST.write_text(header + tokenize.untokenize(out), "utf-8")
print("✅ layer23.py сохранён — импорты и имена упрощены.")