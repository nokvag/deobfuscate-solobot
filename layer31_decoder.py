#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer32_rename_locals.py
  • автоматически переименовывает «рандомные» локальные переменные
      в install_cli → path_launcher, python_exe, search_dirs, bin_dir, script_file, fh
  • меняет while 1 -> while True
  • 493  -> 0o755  (понятнее права файла)
  • результат сохраняет в layer32.py
"""
from __future__ import annotations
import ast, pathlib, astor

SRC = pathlib.Path("layer31.py")
DST = pathlib.Path("layer32.py")
tree = ast.parse(SRC.read_text("utf-8"), SRC.name)

RENAME_MAP = {          # old  -> new
    # install_cli()
    "NufvPSR1AQNx":  "path_launcher",
    "lsHnbTESTPag":  "python_exe",
    "u4Kgw2xftrng":  "search_dirs",
    "LjLi2w1n0i3h":  "bin_dir",
    "DK9LsyO02L_J":  "script_file",
    "HohFPgdHHRgg":  "fh",
    # backup_loop
    # nothing yet – leave
}

class Cleanup(ast.NodeTransformer):
    def visit_Name(self, node: ast.Name):
        if node.id in RENAME_MAP:
            node.id = RENAME_MAP[node.id]
        return node

    def visit_While(self, node: ast.While):
        # while 1  -> while True
        if isinstance(node.test, ast.Constant) and node.test.value == 1:
            node.test = ast.NameConstant(value=True)
        self.generic_visit(node)
        return node

    def visit_Constant(self, node: ast.Constant):
        # 493  -> 0o755  (если точно 493)
        if isinstance(node.value, int) and node.value == 493:
            return ast.copy_location(ast.Constant(value=0o755), node)
        return node

tree = Cleanup().visit(tree)
ast.fix_missing_locations(tree)

# ---------- вывод ----------
code_clean = astor.to_source(tree)
DST.write_text(code_clean, "utf-8")
print("✅ layer32.py создан: локальные имена и мелкие константы приведены к норме.")