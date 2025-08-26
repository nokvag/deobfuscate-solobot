#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer30_cleanup.py
  • заменяет оставшиеся присваивания-импорты на обычные from-import
  • удаляет import importlib, если он больше не нужен
  • результат: layer30.py
"""
from __future__ import annotations
import io, re, pathlib, tokenize

SRC = pathlib.Path("layer29.py")
DST = pathlib.Path("layer30.py")
code = SRC.read_text("utf-8")

# ── 1. найдём «громоздкие» блоки через регэксп ────────────────────────
# они всегда одной из двух форм:
#   (a, b) = (importlib.import_module('pkg.path').a....a,
#             importlib.import_module('pkg.path').b....b)
#   single  = (importlib.import_module('pkg.path').single....single,)
tuple_pat  = re.compile(
    r"^\(([^)]+?)\)\s*=\s*\(\s*importlib\.import_module\('([^']+)'\)"
    r"\.[^.]+\.[^.]+\.[^.]+?\s*,\s*"
    r"importlib\.import_module\('\2'\)\.[^.]+\.[^.]+\.[^.]+?\s*\)",
    re.M  # MULTILINE
)
single_pat = re.compile(
    r"^(\w+)\s*=\s*\(\s*importlib\.import_module\('([^']+)'\)"
    r"\.[^.]+\.[^.]+\.[^.]+?\s*,?\s*\)",
    re.M
)

imports: list[str] = []

def repl_tuple(match: re.Match[str]) -> str:
    left_vars = [v.strip() for v in match.group(1).split(",")]
    pkg       = match.group(2)
    imports.append(f"from {pkg} import {', '.join(left_vars)}")
    return ""  # удалить исходную строку

def repl_single(match: re.Match[str]) -> str:
    var, pkg = match.group(1), match.group(2)
    imports.append(f"from {pkg} import {var}")
    return ""  # удалить исходную строку

code = tuple_pat.sub(repl_tuple, code)
code = single_pat.sub(repl_single, code)

# ── 2. если importlib больше не используется — убрать импорт ─────────
if "importlib.import_module" not in code:
    code = code.replace("import importlib\n", "")

# ── 3. соберём итоговый файл ─────────────────────────────────────────
header = "\n".join(sorted(set(imports))).strip()
if header:
    header += "\n\n"

DST.write_text(header + code.lstrip(), "utf-8")
print("✅ layer30.py готов – оставшиеся importlib-блоки убраны.")