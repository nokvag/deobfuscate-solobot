#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer15_decoder.py
    • ищет кортежные присваивания вида   (X,) = (__import__('asyncio'),)
                                        (A, B) = (getattr(...,'foo'), getattr(...,'bar'))
    • строит карту  obf_name → real_name
    • токенизирует исходник и делает массовое «rename variable»
    • пишет результат в  layer15.py
"""
import io, re, tokenize, ast, pathlib, keyword

SRC = pathlib.Path("layer14.py")
DST = pathlib.Path("layer15.py")
code = SRC.read_text(encoding="utf-8")

# ── 1. грубый парс присваиваний ─────────────────────────────────────────
alias_map: dict[str, str] = {}

assign_re = re.compile(
    r"^\(([^)]+)\)\s*=\s*\((.+)\)$",
    re.MULTILINE)

for m in assign_re.finditer(code):
    left = [v.strip() for v in m.group(1).split(",")]
    right = [s.strip() for s in m.group(2).split(",")]

    for obf, expr in zip(left, right):
        if not obf:   # пустая строка после последней запятой
            continue

        # __import__('pkg.sub')
        imp = re.match(r"__import__\(\s*'([^']+)'\s*\)", expr)
        if imp:
            alias_map[obf] = imp.group(1).split(".")[-1]
            continue

        # getattr(…, 'Something')
        gat = re.search(r"getattr\([^,]+,\s*'([^']+)'\s*\)", expr)
        if gat:
            alias_map[obf] = gat.group(1)
            continue

# отфильтруем конфликтующие / зарезервированные
alias_map = {k: v for k, v in alias_map.items()
             if v.isidentifier() and not keyword.iskeyword(v)}

# ручная защита от дубликатов
seen = {}
for k, v in list(alias_map.items()):
    if v in seen:
        alias_map[k] = f"{v}_{seen[v]}"
        seen[v] += 1
    else:
        seen[v] = 1

print(f"🔎 найдено псевдонимов: {len(alias_map)}")

# ── 2. токен-rename ────────────────────────────────────────────────────
out_tokens = []
stream = io.StringIO(code)
for tok in tokenize.generate_tokens(stream.readline):
    tok_type, tok_str, *rest = tok
    if tok_type == tokenize.NAME and tok_str in alias_map:
        tok_str = alias_map[tok_str]
    out_tokens.append((tok_type, tok_str))

new_code = tokenize.untokenize(out_tokens)

DST.write_text(new_code, encoding="utf-8")
print(f"✅ layer15.py создан — переменные переименованы.")