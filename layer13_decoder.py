#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer13_decoder.py
  • сворачивает любые константные выражения, если в них встречаются
    ТОЛЬКО безопасные built-in-ы;
  • повторно заменяет getattr(obj,"name")   → obj.name
                       getattr(...)(…)      → obj.name(…)
  • результат сохраняет в layer13.py
"""
from __future__ import annotations
import ast, builtins, pathlib, sys

SRC = pathlib.Path("layer12.py")
DST = pathlib.Path("layer13.py")

code = SRC.read_text("utf-8")
tree = ast.parse(code, SRC.name)

# ---------------- «белый список» ----------------
SAFE = {k: getattr(builtins, k) for k in
        ("chr", "ord", "int", "len", "str", "bytes", "ascii", "bool", "bytes")}
SAFE_NAMES = frozenset(SAFE)

# ---------- утилита: разрешён ли узел полностью ----------


def _is_safe(node: ast.AST) -> bool:
    """Все имена внутри node принадлежат SAFE_NAMES?"""
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id not in SAFE_NAMES:
            return False
        if isinstance(n, ast.Attribute):
            return False          # обращений к модулям быть не должно
    return True


def const_fold(node: ast.AST) -> ast.AST:
    """Пробуем вычислить и вернуть ast.Constant"""
    if not _is_safe(node):
        return node
    try:
        val = eval(compile(ast.Expression(node), "<fold>", "eval"),
                   {"__builtins__": SAFE}, {})
        return ast.Constant(value=val)
    except Exception:
        return node


class Folder(ast.NodeTransformer):
    # --- 1. константные операции ------------------------------------
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                ast.MatMult, ast.Div, ast.Mod,
                                ast.Pow, ast.LShift, ast.RShift,
                                ast.BitOr, ast.BitXor, ast.BitAnd,
                                ast.FloorDiv)):
            return const_fold(node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        # попытка 1: сам вызов может быть константой
        if isinstance(node.func, ast.Name) and node.func.id in SAFE_NAMES:
            return const_fold(node)

        # попытка 2: это getattr(obj,"const")(…)
        f = node.func
        if (isinstance(f, ast.Call)
                and isinstance(f.func, ast.Name)
                and f.func.id == "getattr"
                and len(f.args) >= 2
                and isinstance(f.args[1], ast.Constant)
                and isinstance(f.args[1].value, str)):
            obj, name = f.args[0], f.args[1].value
            return ast.copy_location(
                ast.Call(func=ast.Attribute(value=obj, attr=name, ctx=ast.Load()),
                         args=node.args, keywords=node.keywords), node)
        return node

    # одиночный getattr(obj,"const")  →  obj.const
    def visit_Expr(self, node):
        self.generic_visit(node)
        v = node.value
        if (isinstance(v, ast.Call)
                and isinstance(v.func, ast.Name)
                and v.func.id == "getattr"
                and len(v.args) == 2
                and isinstance(v.args[1], ast.Constant)
                and isinstance(v.args[1].value, str)):
            obj, name = v.args
            return ast.copy_location(
                ast.Expr(value=ast.Attribute(value=obj,
                                             attr=name.value,
                                             ctx=ast.Load())), node)
        return node


folder = Folder()
prev, cur = "", tree
while prev != (dump := ast.dump(cur)):
    prev, cur = dump, folder.visit(cur)
    ast.fix_missing_locations(cur)

try:
    new_code = ast.unparse(cur)          # Py ≥3.9
except AttributeError:                   # для 3.8 — через astor
    import astor
    new_code = astor.to_source(cur)

DST.write_text(new_code, "utf-8")
print("✅ layer13.py создан — строки/числа свернуты, getattr заменён.")