#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer8_decoder.py
   • раскрывает вызовы u1KQ2EguJKQ7(b'…') прямо в коде
   • создаёт файл layer8.py
"""
import ast
import pathlib
import re
import sys

SRC = pathlib.Path("layer7.py")
DST = pathlib.Path("layer8.py")
FN  = "u1KQ2EguJKQ7"                  # имя функции-декодера

code = SRC.read_text(encoding="utf-8")

# ────────────────── 1. берём строку с lambda ──────────────────
m_lambda = re.search(rf"^{FN}\s*=\s*lambda.*", code, flags=re.M)
if not m_lambda:
    sys.exit(f"❌ Не нашёл определение {FN} в {SRC}")
lambda_line = m_lambda.group(0)

# ────────────────── 2. компилируем её, получаем функцию ───────
sandbox = {}
exec(lambda_line, sandbox, sandbox)
decode = sandbox[FN]

# ────────────────── 3. меняем вызовы FN(b'…') на строки ───────
PAT = re.compile(rf"{FN}\s*\(\s*(b[\"'](?:\\.|[^\\\"'])*[\"'])\s*\)")

def _replace(match: re.Match) -> str:
    b_literal = match.group(1)               # bytes-литерал как строка
    try:
        raw: bytes = ast.literal_eval(b_literal)
        decoded = decode(raw).decode()
        return repr(decoded)
    except Exception as err:
        print(f"[!] не смог декодировать {b_literal}: {err}", file=sys.stderr)
        return b_literal                      # на крайний случай не меняем

new_code = PAT.sub(_replace, code)

# ────────────────── 4. сохраняем результат ────────────────────
DST.write_text(new_code, encoding="utf-8")
print(f"✅ Готово! Сняли ещё один слой → {DST.resolve()}")