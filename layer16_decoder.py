#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer16_decoder.py
  • строит карту «обфусцированное_имя → настоящее»
    на основе кортежных присваиваний
  • массово переименовывает переменные по токенам
  • сохраняет результат в layer16.py
"""
from __future__ import annotations
import ast, io, keyword, pathlib, tokenize, builtins

SRC = pathlib.Path("layer15.py")
DST = pathlib.Path("layer16.py")

code = SRC.read_text("utf-8")
module = ast.parse(code, SRC.name)

def resolve_name(node: ast.AST) -> str | None:
    """Попытаться вытащить «честное» имя из выражения."""
    # __import__('pkg.sub')
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "__import__"
            and node.args and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        return node.args[0].value.split(".")[-1]

    # getattr(obj, 'Attr')  (берём самый последний константный аргумент)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "getattr" and len(node.args) >= 2
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)):
        return node.args[1].value

    # вложенные getattr(...getattr(...'Attr'))
    if (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "getattr"):
        return resolve_name(node.args[0]) or resolve_name(node.func)

    return None


alias_map: dict[str, str] = {}

for n in module.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1:
        tgt = n.targets[0]
        if isinstance(tgt, ast.Tuple) and isinstance(n.value, ast.Tuple):
            for left_el, right_el in zip(tgt.elts, n.value.elts):
                if isinstance(left_el, ast.Name):
                    real = resolve_name(right_el)
                    if real and real.isidentifier():
                        alias_map[left_el.id] = real

# убираем ключевые слова и дубликаты
reserved = set(keyword.kwlist) | set(dir(builtins))
final_map: dict[str, str] = {}
counter: dict[str, int] = {}
for obf, real in alias_map.items():
    if real in reserved:
        continue
    base = real
    if real in final_map.values():
        counter[base] = counter.get(base, 0) + 1
        real = f"{base}_{counter[base]}"
    final_map[obf] = real

print(f"🔍 собрали {len(final_map)} переименований")

# ---------- токен-замена ----------
out_tokens = []
stream = io.StringIO(code)
for tok in tokenize.generate_tokens(stream.readline):
    ttype, tstr, *rest = tok
    if ttype == tokenize.NAME and tstr in final_map:
        tstr = final_map[tstr]
    out_tokens.append((ttype, tstr, *rest))

DST.write_text(tokenize.untokenize(out_tokens), "utf-8")
print(f"✅ layer16.py сохранён по пути: {DST}")