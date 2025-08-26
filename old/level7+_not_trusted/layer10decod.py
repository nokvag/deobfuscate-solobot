import ast, astor, importlib.util, pathlib, inspect, types

SRC_FILE = pathlib.Path("layer9_folded.py")
SOURCE    = SRC_FILE.read_text()

# ── 1. тащим KEY и xor_transform из уже‑очищенного слоя ────────────────
spec = importlib.util.spec_from_file_location("_stage", SRC_FILE)
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
xor_transform = mod.xor_transform           # та же функция, тот же KEY

# ── 2. AST‑трансформер ────────────────────────────────────────────────
class StringExtractor(ast.NodeTransformer):
    """Pass #3: xor‑decrypt и bytes.decode → константа"""

    # xor_transform(b'....')  ->  Constant(bytes)
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)

        # ❶ xor_transform(b"...")
        if ( isinstance(node.func, ast.Name)
             and node.func.id in {"xor_transform", "encrypt", "decrypt"}
             and len(node.args) >= 1
             and isinstance(node.args[0], ast.Constant)
             and isinstance(node.args[0].value, (bytes, bytearray)) ):
            data = node.args[0].value
            try:
                dec = xor_transform(data)
                return ast.copy_location(ast.Constant(dec), node)
            except Exception:
                pass

        # ❷ b"...".decode("utf-8")
        if ( isinstance(node.func, ast.Attribute)
             and node.func.attr == "decode"
             and isinstance(node.func.value, ast.Constant)
             and isinstance(node.func.value.value, (bytes, bytearray)) ):
            encoding = "utf-8"
            if node.args:
                arg0 = node.args[0]
                if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                    encoding = arg0.value
            try:
                txt = node.func.value.value.decode(encoding)
                return ast.copy_location(ast.Constant(txt), node)
            except Exception:
                pass

        return node

# ── 3. прогоняем ──────────────────────────────────────────────────────
tree = ast.parse(SOURCE)
tree = StringExtractor().visit(tree)
ast.fix_missing_locations(tree)

out = SRC_FILE.with_name("layer9_strings.py")
out.write_text(astor.to_source(tree))
print("✅ xor/byte‑строки раскрыты →", out)