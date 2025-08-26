#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer14_decoder.py
    1. убирает   <str_literal>.decode('utf-8', *[, errors='strict'])
    2. повторно разворачивает   getattr(obj, "name")  → obj.name
                                getattr(obj, "name")(…) → obj.name(…)
    сохраняет результат в layer14.py
"""
from __future__ import annotations
import ast, pathlib, sys, builtins

SRC = pathlib.Path("layer13.py")
DST = pathlib.Path("layer14.py")

code = SRC.read_text("utf-8")
tree = ast.parse(code, SRC.name)

# ─────────────────────────────── helpers ──────────────────────────────
def rm_decode(node: ast.Call) -> ast.AST | None:
    """
    Если node —  <Constant str|bytes>.decode('utf-8' [, errors=...])
    вернуть Constant-узел с готовым str, иначе None.
    """
    if (isinstance(node.func, ast.Attribute)
            and node.func.attr == "decode"
            and isinstance(node.func.value, ast.Constant)
            and (isinstance(node.func.value.value, (str, bytes)))):
        # проверяем аргументы
        if not node.args:
            return ast.Constant(node.func.value.value.decode()   # bytes→str
                                 if isinstance(node.func.value.value, bytes)
                                 else node.func.value.value)      # str остаётся
        if (len(node.args) == 1 and isinstance(node.args[0], ast.Constant)
                and node.args[0].value.lower() in ("utf8", "utf-8")):
            return ast.Constant(
                node.func.value.value.decode("utf-8")              # bytes
                if isinstance(node.func.value.value, bytes)
                else node.func.value.value)                        # str
    return None

SAFE_NAMES = {"chr", "ord", "int", "len", "str", "bytes"}

def safe_eval(expr: ast.AST) -> ast.AST:
    """Попытаться вычислить выражение, если в нём нет посторонних имён."""
    if any(isinstance(n, ast.Name) and n.id not in SAFE_NAMES
           for n in ast.walk(expr)):
        return expr
    try:
        val = eval(compile(ast.Expression(expr), "<eval>", "eval"),
                   {"__builtins__": {n: getattr(builtins, n) for n in SAFE_NAMES}},
                   {})
        return ast.Constant(val)
    except Exception:
        return expr

# ──────────────────────────── Transformer ─────────────────────────────
class Cleaner(ast.NodeTransformer):
    # 1. снимаем .decode(...)
    def visit_Call(self, node):
        self.generic_visit(node)
        replaced = rm_decode(node)
        if replaced is not None:
            return replaced
        # попытка доп. свёртки безопасного вызова
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_NAMES:
            return safe_eval(node)
        # преобразование getattr после возможного decode-фолдинга
        node = self.rewrite_getattr_call(node)
        return node

    # standalone getattr(obj,'name')  → obj.name
    def visit_Expr(self, node):
        self.generic_visit(node)
        val = node.value
        if (isinstance(val, ast.Call)
                and isinstance(val.func, ast.Name) and val.func.id == "getattr"
                and len(val.args) == 2
                and isinstance(val.args[1], ast.Constant)
                and isinstance(val.args[1].value, str)):
            obj, name = val.args
            return ast.copy_location(
                ast.Expr(value=ast.Attribute(value=obj,
                                             attr=name.value,
                                             ctx=ast.Load())),
                node)
        return node

    # helper: getattr(obj,"name")(…)  → obj.name(…)
    @staticmethod
    def rewrite_getattr_call(node: ast.Call) -> ast.Call:
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

# ──────────────────────────── run passes ──────────────────────────────
prev, cur = "", tree
while prev != (dump := ast.dump(cur)):
    prev = dump
    cur = Cleaner().visit(cur)
    ast.fix_missing_locations(cur)

# ─────────────────────────── save result ──────────────────────────────
try:
    new_code = ast.unparse(cur)          # Py ≥3.9
except AttributeError:
    import astor; new_code = astor.to_source(cur)

DST.write_text(new_code, "utf-8")
print("✅ layer14.py создан — .decode() удалены, getattr раскрыт.")