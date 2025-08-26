#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer21_rename_identifiers.py
  • переименовывает обфусцированные функции/переменные
  • изменения в определениях + во всех местах использования
  • результат — layer21.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize

SRC = pathlib.Path("layer20.py")
DST = pathlib.Path("layer21.py")

code = SRC.read_text("utf-8")
tree = ast.parse(code, SRC.name)

# --- 1. карта «старое → новое» ----------------------------------------
RENAME = {
    "QK5bLxBOypkF":      "install_cli",
    "D6P0eecBAFVv":      "backup_loop",
    "M6flxKL4gRoX":      "on_startup",
    "KMS7j9IC8wK5":      "on_shutdown",
    "o_Zg3SYZ2U_F":      "stop_webhooks",
    "WeQFJHP3LH_W":      "main",
    # самые частые временные имена
    "NwVNoYZ0lVgA":      "task",
    "hsEaj3FbHlV3":      "err",
    "aIut2Xl7LjBC":      "sig",
    "CRZYKFwfFJRI":      "stop_event",
    "VEYmCcpb5WZi":      "runner",
    "JutrLWyLwTzT":      "site",
    "SoAy9XMB2LZJ":      "loop",
    "g5gb1yodGaJT":      "pending",
    "fPSFiLwtmvLO":      "bg_tasks",
    "JezwpIWfYHOX":      "expected_secret",
    "_SvfhKl8rD1_":      "is_valid_code",
}

# --- 2. AST-перепись имён --------------------------------------------
class Renamer(ast.NodeTransformer):
    def visit_Name(self, node: ast.Name):
        if node.id in RENAME:
            node.id = RENAME[node.id]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name in RENAME:
            node.name = RENAME[node.name]
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if node.name in RENAME:
            node.name = RENAME[node.name]
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg):
        if node.arg in RENAME:
            node.arg = RENAME[node.arg]
        return node

tree = Renamer().visit(tree)
ast.fix_missing_locations(tree)

# --- 3. сериализация --------------------------------------------------
try:
    new_code = ast.unparse(tree)          # Python ≥ 3.9
except AttributeError:                    # Python 3.8 → astor
    import astor
    new_code = astor.to_source(tree)

# --- 4. доп. замена в строках (f-строки) ------------------------------
#  (unparse уже учёл большинство случаев, но f"{K585qaYUbA_y}{email}"
#   превратил var-имя; однако внутри обычных str.format могло остаться)
for old, new in RENAME.items():
    new_code = new_code.replace(f"{{{old}}}", f"{{{new}}}")

DST.write_text(new_code, "utf-8")
print("✅ layer21.py готов: имена приведены в человеческий вид.")