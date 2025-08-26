#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer24_constfold.py
  • заменяет  fchr(<int>) → '<символ>'
  • сворачивает цепочки 'a' + 'b' + 3*'!' → 'ab!!!'
  • удаляет определение fchr, если он больше не нужен
  результат – layer24.py
"""
from __future__ import annotations
import ast, operator, pathlib

SRC = pathlib.Path("layer23.py")
DST = pathlib.Path("layer24.py")
tree = ast.parse(SRC.read_text("utf-8"), SRC.name)

# ---------- 1. константное fchr ----------
class Fold(ast.NodeTransformer):
    SAFE_BINOP = {
        ast.Add: operator.add,
        ast.Mult: operator.mul,
    }

    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        # fchr(9989)  →  '✅'
        if (isinstance(node.func, ast.Name) and node.func.id == "fchr"
                and len(node.args) == 1
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, int)):
            return ast.copy_location(
                ast.Constant(chr(node.args[0].value)), node)
        return node

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if (type(node.op) in self.SAFE_BINOP
                and isinstance(node.left, ast.Constant)
                and isinstance(node.right, ast.Constant)):
            try:
                val = self.SAFE_BINOP[type(node.op)](
                    node.left.value, node.right.value)
                return ast.copy_location(ast.Constant(val), node)
            except Exception:
                pass
        return node

# многократный проход до стабилизации
prev, cur = "", tree
while prev != (dump := ast.dump(cur)):
    prev, cur = dump, Fold().visit(cur)
    ast.fix_missing_locations(cur)

# ---------- 2. убираем def fchr -----------------
cur.body = [n for n in cur.body
            if not (isinstance(n, ast.FunctionDef) and n.name == "fchr")]

# ---------- 3. serialize ------------------------
try:
    new_code = ast.unparse(cur)
except AttributeError:
    import astor; new_code = astor.to_source(cur)

DST.write_text(new_code, "utf-8")
print("✅ layer24.py создан — строки свёрнуты, fchr удалён.")