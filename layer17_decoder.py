#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer17_decoder.py
  • заменяет  getattr(obj, 'CONST')          → obj.CONST
              getattr(obj, 'CONST')(…)       → obj.CONST(…)
  • раскрывает вызовы  slBqQzRHEsUg('pkg','attr')
      → importlib.import_module('pkg').attr
  • удаляет определение slBqQzRHEsUg, если он больше не используется
  сохраняет результат в layer17.py
"""
from __future__ import annotations
import ast, importlib, pathlib, tokenize, io

SRC = pathlib.Path("layer16.py")
DST = pathlib.Path("layer17.py")

tree = ast.parse(SRC.read_text("utf-8"), SRC.name)

# имя нашей «ленивой» функции
LAZY_FN = "slBqQzRHEsUg"

class Simplifier(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call):
        # сначала обойдём потомков
        self.generic_visit(node)

        # ---------- 1. slBqQzRHEsUg('pkg','attr') ----------
        if (isinstance(node.func, ast.Name) and node.func.id == LAZY_FN
                and len(node.args) >= 2
                and all(isinstance(a, ast.Constant) and isinstance(a.value, str)
                        for a in node.args[:2])):
            pkg, attr = node.args[0].value, node.args[1].value
            new_node = ast.Attribute(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="importlib", ctx=ast.Load()),
                        attr="import_module", ctx=ast.Load()),
                    args=[ast.Constant(value=pkg)], keywords=[]),
                attr=attr, ctx=ast.Load())
            return ast.copy_location(new_node, node)

        # ---------- 2. getattr(obj,'CONST')(…) ----------
        if (isinstance(node.func, ast.Call)
                and isinstance(node.func.func, ast.Name)
                and node.func.func.id == "getattr"
                and len(node.func.args) >= 2
                and isinstance(node.func.args[1], ast.Constant)
                and isinstance(node.func.args[1].value, str)):
            obj  = node.func.args[0]
            name = node.func.args[1].value
            new_func = ast.Attribute(value=obj, attr=name, ctx=ast.Load())
            return ast.copy_location(
                ast.Call(func=new_func, args=node.args, keywords=node.keywords),
                node)

        return node

    def visit_Expr(self, node: ast.Expr):
        """getattr(obj,'CONST')  →  obj.CONST  (без вызова)"""
        self.generic_visit(node)
        val = node.value
        if (isinstance(val, ast.Call)
                and isinstance(val.func, ast.Name) and val.func.id == "getattr"
                and len(val.args) == 2
                and isinstance(val.args[1], ast.Constant)
                and isinstance(val.args[1].value, str)):
            obj, name = val.args
            return ast.copy_location(
                ast.Expr(value=ast.Attribute(value=obj, attr=name.value,
                                             ctx=ast.Load())),
                node)
        return node

# применяем трансформацию «до стабилизации»
prev_dump, cur = "", tree
while prev_dump != (dump := ast.dump(cur)):
    prev_dump, cur = dump, Simplifier().visit(cur)
    ast.fix_missing_locations(cur)

# ---------- 3. если slBqQzRHEsUg более не используется – убираем ----------
class UsageFinder(ast.NodeVisitor):
    def __init__(self): self.used = False
    def visit_Name(self, node):           # noqa: N802
        if node.id == LAZY_FN: self.used = True

finder = UsageFinder(); finder.visit(cur)
if not finder.used:
    cur.body = [n for n in cur.body
                if not (isinstance(n, ast.FunctionDef) and n.name == LAZY_FN)]

# ---------- сохраняем ----------
try:
    new_code = ast.unparse(cur)
except AttributeError:
    import astor
    new_code = astor.to_source(cur)

# добавляем import importlib, если нужен
if "importlib" in new_code and "import importlib" not in new_code:
    new_code = "import importlib\n" + new_code

DST.write_text(new_code, "utf-8")
print(f"✅ layer17.py готов: getattr и slBqQzRHEsUg упрощены.")