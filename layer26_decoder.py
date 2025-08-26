#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer26_fix.py – «точечный» патч для layer26.py
  • заменяет K585qaYUbA_y → SUB_PATH
             Di3ZYNq4y1Jk → WEBHOOK_URL
             err          → exc
  • упрощает импорты вида
        X = (importlib.import_module('pkg.mod').X.pkg.mod.X,)
      →  from pkg.mod import X
  • убирает одноэлементные кортежи-присваивания
  сохраняет результат в layer27.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize

SRC = pathlib.Path("layer26.py")
DST = pathlib.Path("layer27.py")
code = SRC.read_text("utf-8")
tree = ast.parse(code, SRC.name)

# -------- helper: importlib.import_module('pkg').X.X -> ('pkg','X') ---
def parse_import(node: ast.AST) -> tuple[str, str] | None:
    if not isinstance(node, ast.Attribute):
        return None
    attr = node.attr
    base = node.value
    if isinstance(base, ast.Attribute) and base.attr == attr:
        base = base.value                       # убираем X.X
    if (isinstance(base, ast.Call)
            and isinstance(base.func, ast.Attribute)
            and isinstance(base.func.value, ast.Name)
            and base.func.value.id == "importlib"
            and base.func.attr == "import_module"
            and base.args and isinstance(base.args[0], ast.Constant)
            and isinstance(base.args[0].value, str)):
        return base.args[0].value, attr
    return None

imports: list[str] = []
rename: dict[str, str] = {}
new_body: list[ast.stmt] = []

# -------- 1. обрабатываем Assign ------------------------------------------------
for n in tree.body:
    done = False
    if isinstance(n, ast.Assign) and len(n.targets) == 1:
        tgt, val = n.targets[0], n.value

        # снять ( … ,) обёртку
        if isinstance(val, ast.Tuple) and len(val.elts) == 1:
            val = val.elts[0]

        # одиночное имя = importlib...
        if isinstance(tgt, ast.Name):
            info = parse_import(val)
            if info:
                pkg, attr = info
                imports.append(f"from {pkg} import {attr}")
                rename[tgt.id] = attr
                done = True
        # кортеж (a,b) = (importlib..., importlib...)
        elif isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple) \
                and len(tgt.elts) == len(val.elts):
            infos = [parse_import(e) for e in val.elts]
            if all(infos) and len({p for p, _ in infos}) == 1:
                pkg = infos[0][0]
                names = [attr for _, attr in infos]
                imports.append(f"from {pkg} import {', '.join(names)}")
                for l, (_, attr) in zip(tgt.elts, infos):
                    if isinstance(l, ast.Name):
                        rename[l.id] = attr
                done = True
    if not done:
        new_body.append(n)

tree.body = new_body

# -------- 2. сериализуем --------------------------------------------------------
try:
    body_txt = ast.unparse(tree)
except AttributeError:
    import astor; body_txt = astor.to_source(tree)

# -------- 3. глобальная замена имён --------------------------------------------
rename.update({
    "K585qaYUbA_y": "SUB_PATH",
    "Di3ZYNq4y1Jk": "WEBHOOK_URL",
    "err": "exc",
})

tokens_out = []
for tok in tokenize.generate_tokens(io.StringIO(body_txt).readline):
    typ, string, *rest = tok
    if typ == tokenize.NAME and string in rename:
        string = rename[string]
    tokens_out.append((typ, string, *rest))

header = "\n".join(sorted(set(imports))) + ("\n\n" if imports else "")
DST.write_text(header + tokenize.untokenize(tokens_out), "utf-8")
print("✅ layer27.py готов – все «кубики» заменены, импорты нормализованы.")