#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer10_decoder.py
    Константно сворачивает строки/числа в layer9.py,
    записывает результат в layer10.py
"""
import ast
import pathlib
import types
import sys

SRC = pathlib.Path("layer9.py")
DST = pathlib.Path("layer10.py")

code = SRC.read_text(encoding="utf-8")
tree = ast.parse(code, SRC.name)

# Мини-песочница для безопасного eval
SAFE_BUILTINS: dict[str, object] = {
    "chr": chr,
    "ord": ord,
    "len": len,
    "int": int,
    "str": str,
    "bytes": bytes,
}

class ConstantFolder(ast.NodeTransformer):
    def _try_eval(self, node: ast.AST) -> ast.AST:
        """Пробуем вычислить выражение, если оно не содержит Name/Attr."""
        if any(isinstance(n, (ast.Name, ast.Attribute)) for n in ast.walk(node)):
            return node
        try:
            value = eval(compile(ast.Expression(node), "<fold>", "eval"),
                         {"__builtins__": SAFE_BUILTINS}, {})
            return ast.copy_location(ast.Constant(value=value), node)
        except Exception:
            return node

    # ——— сворачиваем BinOp "+" Constant+Constant ———
    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                return self._try_eval(node)
        return node

    # ——— сворачиваем вызовы safe-builtins ———
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Name)
                and node.func.id in SAFE_BUILTINS
                and all(isinstance(arg, ast.Constant) for arg in node.args)
                and all(isinstance(kw.value, ast.Constant) for kw in node.keywords)):
            return self._try_eval(node)
        return node

changed = True
while changed:
    new_tree = ConstantFolder().visit(tree)
    ast.fix_missing_locations(new_tree)
    changed = ast.dump(tree) != ast.dump(new_tree)
    tree = new_tree

# ——— сохраняем результат ———
try:
    new_code = ast.unparse(tree)           # Python ≥3.9
except AttributeError:                     # Python 3.8 → astor
    import astor
    new_code = astor.to_source(tree)

DST.write_text(new_code, encoding="utf-8")
print(f"✅ Константы свёрнуты, файл сохранён: {DST.resolve()}")