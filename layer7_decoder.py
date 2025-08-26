#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer7_decoder.py
  • строим минимальный namespace с нужными псевдонимами
  • компилируем строку `u1KQ2EguJKQ7 = lambda …` без внешних импортов
  • заменяем все вызовы u1KQ2EguJKQ7(b'...') обычными строками
  • сохраняем layer7.py
"""
import ast, builtins, pathlib, re, sys

SRC = pathlib.Path("layer6.py")
DST = pathlib.Path("layer7.py")
CODER = "u1KQ2EguJKQ7"

text = SRC.read_text(encoding="utf-8")

# ────────────────────────────────────────────────────────────────
# 1. отделяем «картошку» (1-ю строку) и сам код
first_nl = text.find("\n")
header   = text[:first_nl]       # огромный список псевдонимов = builtins
body     = text[first_nl + 1:]

# ────────────────────────────────────────────────────────────────
# 2. найдём строку с нашим lambda
m = re.search(rf"^{CODER}\s*=\s*lambda.*", body, flags=re.M)
if not m:
    sys.exit(f"❌ не найдено определение {CODER}")
lambda_line = m.group(0)

# ────────────────────────────────────────────────────────────────
# 3. построй минимальный sandbox
fake_part, real_part = header.split("=", 1)
fake_names = [n.strip() for n in fake_part.split(",")]
real_names = [n.strip() for n in real_part.split(",")]

alias_map = dict(zip(fake_names, real_names))

# какие псевдонимы реально нужны внутри lambda?
needed_aliases = set(re.findall(r"\b[A-Za-z_]\w*\b", lambda_line))
sandbox = {}
for fake in needed_aliases:
    real = alias_map.get(fake)
    if real and hasattr(builtins, real):
        sandbox[fake] = getattr(builtins, real)

# ────────────────────────────────────────────────────────────────
# 4. компилируем lambda-строку
exec(lambda_line, sandbox, sandbox)
decode_func = sandbox[CODER]

# ────────────────────────────────────────────────────────────────
# 5. подменяем вызовы CODER(b"...") на строки
PAT = re.compile(rf"{CODER}\s*\(\s*(b[\"'](?:\\.|[^\\\"'])*[\"'])\s*\)")

def repl(m):
    b_lit = m.group(1)
    try:
        raw = ast.literal_eval(b_lit)           # bytes
        return repr(decode_func(raw).decode())  # str-литерал
    except Exception as exc:
        print(f"[!] не смог декодировать {b_lit}: {exc}", file=sys.stderr)
        return b_lit

result = PAT.sub(repl, body)

DST.write_text(result, encoding="utf-8")
print(f"✅ layer7.py создан: {DST.resolve()}")