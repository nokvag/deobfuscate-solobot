#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer11_decoder.py
  • сворачивает константы
  • превращает  getattr(obj, "name")(…) → obj.name(…)
               getattr(obj, "name")    → obj.name
"""
import ast, pathlib, sys

SRC = pathlib.Path("layer10.py")
DST = pathlib.Path("layer11.py")

code = SRC.read_text(encoding="utf-8")
tree = ast.parse(code, SRC.name)

SAFE_BUILTINS = {"chr": chr, "ord": ord, "len": len,
                 "int": int, "str": str, "bytes": bytes}

def const_eval(node: ast.AST) -> ast.AST:
    if any(isinstance(n, (ast.Name, ast.Attribute)) for n in ast.walk(node)):
        return node
    try:
        v = eval(compile(ast.Expression(node), "<eval>", "eval"),
                 {"__builtins__": SAFE_BUILTINS}, {})
        return ast.Constant(value=v)
    except Exception:
        return node

class Rewriter(ast.NodeTransformer):
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            return const_eval(node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)

        # если сам .func = getattr(obj,"attr")
        f = node.func
        if (isinstance(f, ast.Call) and isinstance(f.func, ast.Name)
                and f.func.id == "getattr"
                and len(f.args) >= 2
                and isinstance(f.args[1], ast.Constant)
                and isinstance(f.args[1].value, str)):
            obj, attr = f.args[0], f.args[1].value
            new_func = ast.Attribute(value=obj, attr=attr, ctx=ast.Load())
            return ast.copy_location(
                ast.Call(func=new_func, args=node.args, keywords=node.keywords), node)

        return node

    def visit_Expr(self, node):
        # одиночный getattr(obj,"attr")  →  obj.attr
        if (isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "getattr"
                and len(node.value.args) == 2
                and isinstance(node.value.args[1], ast.Constant)
                and isinstance(node.value.args[1].value, str)):
            obj, attr = node.value.args
            return ast.copy_location(
                ast.Expr(value=ast.Attribute(value=obj,
                                             attr=attr.value,
                                             ctx=ast.Load())),
                node)
        return self.generic_visit(node)

rewriter = Rewriter()
prev, cur = "", tree
while prev != (dump := ast.dump(cur)):
    prev = dump
    cur = rewriter.visit(cur)
    ast.fix_missing_locations(cur)

try:
    new_code = ast.unparse(cur)          # Py ≥3.9
except AttributeError:
    import astor; new_code = astor.to_source(cur)

DST.write_text(new_code, encoding="utf-8")
print("✅ layer11.py создан: getattr и константы раскрыты.")