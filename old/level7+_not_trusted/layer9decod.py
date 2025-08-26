import ast, astor, pathlib, builtins, operator, textwrap

SRC = pathlib.Path("layer9.py").read_text()

SAFE_GLOBALS = {
    "chr": chr,
    "int": int,
    "ord": ord,
    "True": True,
    "False": False,
    "None": None,
}

BIN_OPS = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.MatMult: operator.matmul,
    ast.Div:  operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod:  operator.mod,
    ast.Pow:  operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.BitAnd: operator.and_,
}

class ConstantFolder(ast.NodeTransformer):
    """‑‑ Pass #2: сворачиваем литералы и decode()‑обёртки."""

    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            op_fn = BIN_OPS.get(type(node.op))
            if op_fn is not None:
                try:
                    return ast.Constant(value=op_fn(node.left.value, node.right.value))
                except Exception:
                    pass  # не получилось ‑ оставляем
        return node

    # ''.join([...]) встречается редко, но иногда полезно
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)

        # decode(...)  ->  Константа
        if isinstance(node.func, ast.Name) and node.func.id == "decode":
            if len(node.args) == 1 and isinstance(node.args[0], ast.Constant):
                return ast.copy_location(ast.Constant(node.args[0].value), node)

        # int("<something>", base)
        if (
            isinstance(node.func, ast.Name) and node.func.id == "int" and
            len(node.args) >= 1 and isinstance(node.args[0], ast.Constant)
        ):
            try:
                value = int(node.args[0].value, *(arg.value for arg in node.args[1:]))
                return ast.Constant(value=value)
            except Exception:
                pass

        # chr(<const>)   ->  'A'
        if isinstance(node.func, ast.Name) and node.func.id == "chr":
            if len(node.args) == 1 and isinstance(node.args[0], ast.Constant):
                try:
                    return ast.Constant(chr(node.args[0].value))
                except Exception:
                    pass

        return node

    def visit_Expr(self, node: ast.Expr):
        # выкидываем shim‑decode, он начинается с "def decode("
        if (
            isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and node.value.value.startswith("def decode(")
        ):
            return None
        return node

# ---------- запускаем трансформацию ----------
tree = ast.parse(SRC)
tree = ConstantFolder().visit(tree)
ast.fix_missing_locations(tree)

OUT = pathlib.Path("layer9_folded.py")
OUT.write_text(astor.to_source(tree))
print("✅ Константы свёрнуты →", OUT)