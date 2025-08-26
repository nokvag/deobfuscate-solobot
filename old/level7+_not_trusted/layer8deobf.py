import ast, astor, pathlib, textwrap, builtins

SRC = pathlib.Path("layer8.py").read_text()

class DeObf(ast.NodeTransformer):
    """
    1. ищем   getattr(<bytes>, <expr>) (<args>)
    2. eval‑им  <expr>        →   'decode'
    3. eval‑им  <bytes> .decode(...)  → строку‑литерал
    4. подменяем всё выражение на ast.Call(
          func=ast.Name(id='decode', ctx=ast.Load()),
          args=[<ранее было внутри скобок>],
          keywords=[]
       )
       ── т.е. то же самое, что вы сделали regex‑ом, но корректно.
    """
    def visit_Call(self, node: ast.Call):
        # ➊ рекурсивно обходим детей
        self.generic_visit(node)

        # ➋ pattern‑match:  getattr( <bytes>, <...> )( <something> )
        if (
            isinstance(node.func, ast.Call) and
            isinstance(node.func.func, ast.Name) and
            node.func.func.id == "getattr" and
            len(node.func.args) == 2 and
            isinstance(node.func.args[0], ast.Constant) and
            isinstance(node.func.args[0].value, (bytes, bytearray))
        ):
            bytes_obj = node.func.args[0].value

            # пытаемся вычислить второй аргумент (обычно набор chr(...) )
            try:
                expr_code = compile(
                    ast.Expression(node.func.args[1]), filename="<deobf>", mode="eval"
                )
                attr_name = eval(expr_code, {"chr": chr})
            except Exception:
                return node         # не получилось — оставляем как есть

            if attr_name == "decode":
                # формируем новый ast.Call:  decode(<old args>)
                return ast.Call(
                    func=ast.Name(id="decode", ctx=ast.Load()),
                    args=node.args,
                    keywords=[],
                )

        return node

# --- запускаем трансформацию ---
tree = ast.parse(SRC)
tree = DeObf().visit(tree)
ast.fix_missing_locations(tree)

# ➌ добавляем shim‑функцию, как выше
shim = textwrap.dedent("""
def decode(obj, *a, **kw):
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj
""")
tree.body.insert(0, ast.parse(shim))

OUT = pathlib.Path("layer8_clean.py")
OUT.write_text(astor.to_source(tree))
print("✅ Готово:", OUT)