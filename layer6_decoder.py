#!/usr/bin/env python3
# deobfuscate_layer5.py
import io, tokenize, token, keyword, builtins, re, sys
from pathlib import Path

SRC  = Path("layer5.py").read_text(encoding="utf-8")
OUT  = Path("layer6.py")

def extract_alias_table(src: str):
    header = src.split("=", 1)
    if len(header) < 2:
        return {}
    left, right_with_nl = header[0], header[1]
    left_names  = [n.strip() for n in left.split(",")]
    right_names = [n.strip() for n in right_with_nl.split("\n", 1)[0].split(",")]

    real_names = right_names          # ← фикс

    return dict(zip(left_names, real_names))

ALIASES = extract_alias_table(SRC)

# некоторые имена хотим оставить «как есть»
KEEP = {"print", "open", "len", "range", "getattr"}
ALIASES = {k: v for k, v in ALIASES.items() if v not in KEEP}

def translate_code(src: str, mapping: dict) -> str:
    result_tokens = []
    g = tokenize.generate_tokens(io.StringIO(src).readline)

    for tok_type, tok_str, *_ in g:
        # меняем только идентификаторы, не трогаем строки/числа/ключевые слова
        if (tok_type == token.NAME
                and tok_str in mapping
                and tok_str not in keyword.kwlist):
            tok_str = mapping[tok_str]
        result_tokens.append((tok_type, tok_str))

    return tokenize.untokenize(result_tokens)

clean_code = translate_code(SRC, ALIASES)
OUT.write_text(clean_code, encoding="utf-8")
print(f"✅ layer6.py готов: {OUT.resolve()}")