#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer19_cleanup.py
  • заменяет (foo,) = (importlib.import_module('pkg').foo.foo,)
          ->  from pkg import foo          # и простое присваивание
  • убирает лишний двойной `.foo.foo`
  • сводит одно-элементные кортежи к обычным именинам
  • переименовывает K585qaYUbA_y -> SUB_PATH
  • сохраняет результат в layer19.py
"""
from __future__ import annotations
import ast, pathlib, tokenize, io, textwrap, keyword

SRC = pathlib.Path("layer18.py")
DST = pathlib.Path("layer19.py")
code = SRC.read_text("utf-8")
mod  = ast.parse(code, SRC.name)

# ────────── 1. раскатываем (x,) = (...) в простое x = ... ───────────
for node in mod.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        tgt = node.targets[0]
        if isinstance(tgt, ast.Tuple) and len(tgt.elts) == 1:
            node.targets[0] = tgt.elts[0]      # превращаем кортеж -> имя

# ────────── 2. ищем importlib.import_module('pkg').attr.attr ────────
def simplify_import(expr: ast.AST) -> tuple[str,str]|None:
    """
    Если expr == importlib.import_module('pkg').attr(.attr)
    вернуть ('pkg','attr')
    """
    if not isinstance(expr, ast.Attribute):
        return None
    attr2 = expr.attr
    val = expr.value
    # возможен двойной .attr.attr
    if isinstance(val, ast.Attribute) and val.attr == attr2:
        val = val.value
    if isinstance(val, ast.Call
                 ) and isinstance(val.func, ast.Attribute
                 ) and val.func.attr == "import_module" \
                 and isinstance(val.func.value, ast.Name) \
                 and val.func.value.id == "importlib" \
                 and val.args and isinstance(val.args[0], ast.Constant) \
                 and isinstance(val.args[0].value, str):
        pkg = val.args[0].value
        return pkg, attr2
    return None

imports: list[tuple[str,str]] = []          # (pkg, name)
replacements: dict[str, str] = {}           # obf_name -> name (для токенов)

for node in mod.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        obf = node.targets[0].id
        simp = simplify_import(node.value)
        if simp:
            pkg, name = simp
            imports.append((pkg, name))
            replacements[obf] = name
            # упростим правую часть до просто name
            node.value = ast.Name(id=name, ctx=ast.Load())

# ────────── 3. подготавливаем блок from-importов ────────────────────
import_lines: list[str] = []
for pkg, name in sorted(set(imports)):
    # «from pkg import name» (избегаем ключевых слов)
    alias = name if not keyword.iskeyword(name) else f"{name}_"
    import_lines.append(f"from {pkg} import {name} as {alias}")

prelude = "\n".join(import_lines) + "\n\n" if import_lines else ""

# ────────── 4. сериализация AST -> code ─────────────────────────────
try:
    new_body = ast.unparse(mod)
except AttributeError:
    import astor
    new_body = astor.to_source(mod)

# ────────── 5. токен-переименование и финальный вывод ───────────────
replacements["K585qaYUbA_y"] = "SUB_PATH"

out_tok = []
stream = io.StringIO(new_body)
for tok in tokenize.generate_tokens(stream.readline):
    typ, string, *rest = tok
    if typ == tokenize.NAME and string in replacements:
        string = replacements[string]
    out_tok.append((typ, string, *rest))

DST.write_text(prelude + tokenize.untokenize(out_tok), "utf-8")
print(f"✅ layer19.py создан — импорты упорядочены, SUB_PATH переименован.")