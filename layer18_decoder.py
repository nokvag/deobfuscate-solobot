#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer18_cleaner.py
  • превращает все оставшиеся  getattr(obj, 'CONST')  → obj.CONST
  • заменяет  K585qaYUbA_y  → SUB_PATH
  • удаляет неиспользуемую функцию  u1KQ2EguJKQ7
  результат сохраняет в layer18.py
"""
from __future__ import annotations
import ast, io, pathlib, tokenize

SRC = pathlib.Path("layer17.py")
DST = pathlib.Path("layer18.py")

code = SRC.read_text("utf-8")
tree = ast.parse(code, SRC.name)

# ───────── 1. AST-перепись getattr(obj,'CONST') → obj.CONST ──────────
class GetAttrConst(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Name) and node.func.id == "getattr"
                and len(node.args) == 2
                and isinstance(node.args[1], ast.Constant)
                and isinstance(node.args[1].value, str)):
            obj, name = node.args
            return ast.copy_location(
                ast.Attribute(value=obj, attr=node.args[1].value,
                              ctx=ast.Load()),
                node)
        return node

tree = GetAttrConst().visit(tree)
ast.fix_missing_locations(tree)

# ───────── 2. удаляем функцию u1KQ2EguJKQ7 ──────────
tree.body = [n for n in tree.body
             if not (isinstance(n, ast.Assign) and
                     any(isinstance(t, ast.Name) and t.id == "u1KQ2EguJKQ7"
                         for t in n.targets))
             and not (isinstance(n, ast.FunctionDef) and n.name == "u1KQ2EguJKQ7")]

# ───────── 3. токен-rename K585qaYUbA_y → SUB_PATH ──────────
TOK_RENAME = {"K585qaYUbA_y": "SUB_PATH"}

tok_out = []
for tok in tokenize.generate_tokens(io.StringIO(ast.unparse(tree)).readline):
    ttype, tstr, *rest = tok
    if ttype == tokenize.NAME and tstr in TOK_RENAME:
        tstr = TOK_RENAME[tstr]
    tok_out.append((ttype, tstr, *rest))

DST.write_text(tokenize.untokenize(tok_out), "utf-8")
print("✅ layer18.py готов: getattr развёрнут, мусор убран.")