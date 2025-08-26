#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer20_import_fix.py
  • заменяет присваивания формата
        asyncio = (__import__('asyncio'),)
        router  = (importlib.import_module('handlers').router.router,)
        foo, bar = ( ..., ... )
    на эквивалентные инструкции импорта + обычные имена
  • убирает лишний двойной '.attr.attr'
  • сохраняет результат в layer20.py
"""
from __future__ import annotations
import ast, keyword, pathlib, textwrap

SRC = pathlib.Path("layer19.py")
DST = pathlib.Path("layer20.py")
code = SRC.read_text("utf-8")
module = ast.parse(code, SRC.name)

# ───────────────── helpers ──────────────────────
def extract_name(node: ast.AST) -> tuple[str, str] | None:
    """
    Если node = importlib.import_module('pkg').attr(.attr)
         или     __import__('pkg.sub')
    вернуть (pkg, attr_or_pkg)
    """
    # __import__('pkg.sub')
    if (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "__import__"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        pkg = node.args[0].value
        return pkg, pkg.split(".")[-1]

    # importlib.import_module('pkg').attr(.attr)
    if isinstance(node, ast.Attribute):
        final_attr = node.attr
        val = node.value
        # устранить повтор .attr.attr
        if isinstance(val, ast.Attribute) and val.attr == final_attr:
            val = val.value
        if (isinstance(val, ast.Call)
                and isinstance(val.func, ast.Attribute)
                and isinstance(val.func.value, ast.Name)
                and val.func.value.id == "importlib"
                and val.func.attr == "import_module"
                and val.args
                and isinstance(val.args[0], ast.Constant)
                and isinstance(val.args[0].value, str)):
            pkg = val.args[0].value
            return pkg, final_attr
    return None

# ───── 1. собираем импорты и готовим подмены ─────
imports: list[str] = []          # «строки with import»
rename: dict[str, str] = {}      # old_var -> good_name
new_body: list[ast.stmt] = []

for node in module.body:
    handled = False
    if (isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)):
        var = node.targets[0].id
        expr = node.value
        # разворачиваем одноэлементный кортеж
        if isinstance(expr, ast.Tuple) and len(expr.elts) == 1:
            expr = expr.elts[0]
        data = extract_name(expr)
        if data:
            pkg, name = data
            # избегаем ключевых слов
            alias = name if not keyword.iskeyword(name) else f"{name}_"
            if pkg == name:                  # обычный «import pkg»
                imports.append(f"import {pkg} as {alias}"
                                if alias != pkg else f"import {pkg}")
            else:                            # from pkg import name
                imports.append(f"from {pkg} import {name}"
                                + (f" as {alias}" if alias != name else ""))
            rename[var] = alias
            handled = True
    if not handled:
        new_body.append(node)

module.body = new_body  # заменяем модуль-body

# ───── 2. сериализуем AST ─────
try:
    body_code = ast.unparse(module)
except AttributeError:  # Py < 3.9
    import astor
    body_code = astor.to_source(module)

# ───── 3. текстовая замена имён переменных ─────
for old, new in rename.items():
    body_code = body_code.replace(old, new)

import_block = "\n".join(sorted(set(imports))) + "\n\n"
DST.write_text(import_block + body_code, "utf-8")
print(f"✅ layer20.py создан: импорты распрямлены, имена оживлены.")