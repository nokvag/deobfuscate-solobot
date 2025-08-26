#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer25_cleanup.py
  • превращает громоздкие присваивания на базе
      importlib.import_module('pkg').attr(.attr)
    в   from pkg import attr
  • убирает одноэлементные кортежи-присваивания
  • глобально переименовывает:
        K585qaYUbA_y -> SUB_PATH
        Di3ZYNq4y1Jk -> webhook_url
        err          -> exc
  • пишет результат в layer25.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize, keyword

SRC = pathlib.Path("layer24.py")
DST = pathlib.Path("layer25.py")
code = SRC.read_text("utf-8")
mod  = ast.parse(code, SRC.name)

# ---------- helpers ---------------------------------------------------
def split_import(node: ast.AST) -> tuple[str, str] | None:
    """
    Распознать конструкцию
      importlib.import_module('pkg.sub').attr(.attr)
    вернуть ('pkg.sub', 'attr')
    """
    if not isinstance(node, ast.Attribute):
        return None
    attr = node.attr
    base = node.value
    if isinstance(base, ast.Attribute) and base.attr == attr:
        base = base.value                     # убираем двойной .attr.attr
    if (isinstance(base, ast.Call) and isinstance(base.func, ast.Attribute)
            and isinstance(base.func.value, ast.Name)
            and base.func.value.id == "importlib"
            and base.func.attr == "import_module"
            and base.args and isinstance(base.args[0], ast.Constant)
            and isinstance(base.args[0].value, str)):
        return base.args[0].value, attr
    return None

imports: list[str] = []            # строки готовых import / from-import
rename:  dict[str, str] = {}       # obf → new_name
new_body: list[ast.stmt] = []

# ---------- 1. разворачиваем Assign-импорты ---------------------------
for node in mod.body:
    handled = False
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        tgt = node.targets[0]
        val = node.value

        # «снять» одноэлементный кортеж
        if isinstance(val, ast.Tuple) and len(val.elts) == 1:
            val = val.elts[0]

        # (a, b, …) = (importlib …, importlib …, …)
        if isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple) \
                and len(tgt.elts) == len(val.elts):
            parts = [split_import(v) for v in val.elts]
            if all(parts) and len({p for p, _ in parts}) == 1:
                pkg = parts[0][0]
                names = [attr for _, attr in parts]
                imports.append(f"from {pkg} import {', '.join(names)}")
                for l, (_, attr) in zip(tgt.elts, parts):
                    if isinstance(l, ast.Name):
                        rename[l.id] = attr
                handled = True

        # одиночное   x = importlib.import_module(...).attr(.attr)
        elif isinstance(tgt, ast.Name):
            info = split_import(val)
            if info:
                pkg, attr = info
                alias = attr if not keyword.iskeyword(attr) else f"{attr}_"
                if alias == attr:
                    imports.append(f"from {pkg} import {attr}")
                else:
                    imports.append(f"from {pkg} import {attr} as {alias}")
                rename[tgt.id] = alias
                handled = True

    if not handled:
        new_body.append(node)

mod.body = new_body

# ---------- 2. сериализуем обратно -----------------------------------
try:
    body = ast.unparse(mod)        # Py ≥ 3.9
except AttributeError:
    import astor; body = astor.to_source(mod)

# ---------- 3. глобальные переименования ------------------------------
rename.update({
    "K585qaYUbA_y": "SUB_PATH",
    "Di3ZYNq4y1Jk": "webhook_url",
    "err":          "exc",          # фикс в print/логах
})

out_tok = []
stream = io.StringIO(body)
for tok in tokenize.generate_tokens(stream.readline):
    typ, string, *rest = tok
    if typ == tokenize.NAME and string in rename:
        string = rename[string]
    out_tok.append((typ, string, *rest))

header = "\n".join(sorted(set(imports))) + ("\n\n" if imports else "")
DST.write_text(header + tokenize.untokenize(out_tok), "utf-8")
print("✅  layer25.py создан — импорты упрощены, имена добиты.")