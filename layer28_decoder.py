#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer29_cleanup.py
  • превращает все конструкции вида
        (a, b) = (importlib.import_module('pkg').a.pkg.a,
                  importlib.import_module('pkg').b.pkg.b)
        x = (importlib.import_module('pkg.mod').x.pkg.mod.x,)
    в нормальные "from … import …" и обычные переменные-ссылки
  • удаляет строку "import importlib" если она больше не нужна
  сохраняет результат в layer29.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize, textwrap

SRC = pathlib.Path("layer28.py")
DST = pathlib.Path("layer29.py")

source = SRC.read_text("utf-8")
module = ast.parse(source, SRC.name)

# ───────── helpers ─────────
def from_import(node: ast.AST) -> tuple[str, str] | None:
    """распознаёт  importlib.import_module('pkg').attr(.attr)"""
    if not isinstance(node, ast.Attribute):
        return None
    attr = node.attr
    head = node.value
    if isinstance(head, ast.Attribute) and head.attr == attr:
        head = head.value                       # убираем ".attr.attr"
    if (isinstance(head, ast.Call)
            and isinstance(head.func, ast.Attribute)
            and isinstance(head.func.value, ast.Name)
            and head.func.value.id == "importlib"
            and head.func.attr == "import_module"
            and head.args
            and isinstance(head.args[0], ast.Constant)
            and isinstance(head.args[0].value, str)):
        return head.args[0].value, attr
    return None

imports: list[str] = []
new_body: list[ast.stmt] = []

for node in module.body:
    rewritten = False
    # ── одно или несколько имён слева ────────────────────────────────
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        lhs, rhs = node.targets[0], node.value
        # x = ( … ,)  →  распаковываем
        if isinstance(rhs, ast.Tuple) and len(rhs.elts) == 1:
            rhs = rhs.elts[0]

        # 1) кортеж (a,b) = (import…, import…)
        if isinstance(lhs, ast.Tuple) and isinstance(rhs, ast.Tuple) \
                and len(lhs.elts) == len(rhs.elts):
            infos = [from_import(e) for e in rhs.elts]
            if all(infos) and len({p for p, _ in infos}) == 1:
                pkg = infos[0][0]
                names = [a for _, a in infos]
                imports.append(f"from {pkg} import {', '.join(names)}")
                rewritten = True

        # 2) одиночное  name = importlib…
        elif isinstance(lhs, ast.Name):
            info = from_import(rhs)
            if info:
                pkg, attr = info
                imports.append(f"from {pkg} import {attr}")
                rewritten = True

    if not rewritten:
        new_body.append(node)

module.body = new_body

# ───────── сериализуем back ─────────
try:
    body_txt = ast.unparse(module)
except AttributeError:
    import astor; body_txt = astor.to_source(module)

# ───────── удаляем лишний "import importlib" ─────────
if "importlib" not in body_txt:
    body_txt = body_txt.replace("import importlib\n", "")

header = "\n".join(sorted(set(imports))) + ("\n\n" if imports else "")
DST.write_text(header + body_txt.lstrip(), "utf-8")
print("✅ layer29.py создан — последние importlib-костыли убраны.")