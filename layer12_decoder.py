#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer12_decoder.py – сворачиваем все остаточные константы
и вновь превращаем getattr-конструкции в нормальный вид.

результат → layer12.py
"""
import ast, pathlib, builtins

SRC = pathlib.Path("layer11.py")
DST = pathlib.Path("layer12.py")
tree = ast.parse(SRC.read_text("utf-8"), SRC.name)

# ───── безопасный набор функций, разрешённых для eval ─────
SAFE = {k: getattr(builtins, k)
        for k in ("chr", "ord", "int", "len", "str", "bytes", "ascii")}

def try_eval(node: ast.AST) -> ast.AST:
    """Попытка вычислить узел -> ast.Constant, если там нет имён."""
    if any(isinstance(n, (ast.Name, ast.Attribute))
           for n in ast.walk(node)):
        return node
    try:
        value = eval(compile(ast.Expression(node), "<fold>", "eval"),
                     {"__builtins__": SAFE}, {})
    except Exception:
        return node
    return ast.Constant(value=value)

class Folder(ast.NodeTransformer):
    # 1) сворачиваем BinOp (`+`) и вызовы SAFE-функций
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Add):
            return try_eval(node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        # если зовут безопасную функцию – сворачиваем
        if isinstance(node.func, ast.Name) and node.func.id in SAFE:
            return try_eval(node)
        # если сам call = getattr(obj,"const")(…) – обработаем ниже
        return node

    # 2) getattr(obj,"const")(…)  и  getattr(obj,"const")
    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if (isinstance(f, ast.Call) and isinstance(f.func, ast.Name)
                and f.func.id == "getattr"
                and len(f.args) >= 2
                and isinstance(f.args[1], ast.Constant)
                and isinstance(f.args[1].value, str)):
            obj, name = f.args[0], f.args[1].value
            new_func = ast.Attribute(value=obj, attr=name, ctx=ast.Load())
            return ast.copy_location(
                ast.Call(func=new_func, args=node.args, keywords=node.keywords),
                node)
        return node

    def visit_Expr(self, node):
        self.generic_visit(node)
        v = node.value
        if (isinstance(v, ast.Call)
                and isinstance(v.func, ast.Name) and v.func.id == "getattr"
                and len(v.args) == 2
                and isinstance(v.args[1], ast.Constant)
                and isinstance(v.args[1].value, str)):
            obj, name = v.args
            return ast.copy_location(
                ast.Expr(value=ast.Attribute(value=obj, attr=name.value,
                                             ctx=ast.Load())), node)
        return node

folder = Folder()
prev_dump, cur = "", tree
while prev_dump != (d := ast.dump(cur)):
    prev_dump = d
    cur = folder.visit(cur)
    ast.fix_missing_locations(cur)

# ───── печать / сохранение ─────
try:
    new_code = ast.unparse(cur)      # Python ≥3.9
except AttributeError:
    import astor; new_code = astor.to_source(cur)

DST.write_text(new_code, "utf-8")
print("✅ layer12.py создан – константы раскрыты, getattr заменён.")