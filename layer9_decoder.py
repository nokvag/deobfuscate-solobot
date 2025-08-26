#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer9_decoder.py
    заменяет *все* вызовы u1KQ2EguJKQ7(b'…') на обычные строковые
    пишет результат в layer9.py
"""
import ast
import pathlib
import sys

SRC = pathlib.Path("layer8.py")      # что разбираем
DST = pathlib.Path("layer9.py")      # что создаём
FN  = "u1KQ2EguJKQ7"                 # функция-декодер в файле

code = SRC.read_text(encoding="utf-8")

# ───────── получить саму функцию-декодер ──────────
mod = ast.parse(code, SRC.name)
decode_node = next(
    n for n in mod.body
    if isinstance(n, ast.Assign)
       and any(isinstance(t, ast.Name) and t.id == FN for t in n.targets)
)

# исполняем правую часть присваивания, чтобы получить lambda-функцию
sandbox = {}
exec(compile(ast.Module([decode_node], type_ignores=[]), "<lambda>", "exec"),
     sandbox, sandbox)
decode = sandbox[FN]                      # теперь это callable

# ────────── трансформер для дерева ────────────
class CallRewriter(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)          # сначала обработать вложенные
        # интересует: FN(b'...')  (один позиционный аргумент-bytes)
        if (isinstance(node.func, ast.Name)
                and node.func.id == FN
                and len(node.args) == 1
                and isinstance(node.args[0], ast.Bytes)):
            raw_bytes = node.args[0].s            # значение bytes
            try:
                decoded = decode(raw_bytes).decode("utf-8", "replace")
                return ast.copy_location(ast.Constant(value=decoded), node)
            except Exception as err:
                print(f"[skip] не смог декодировать {raw_bytes!r}: {err}",
                      file=sys.stderr)
        return node

new_tree = CallRewriter().visit(mod)
ast.fix_missing_locations(new_tree)

# ────────── сохранить результат ────────────
try:
    new_code = ast.unparse(new_tree)      # Py ≥3.9
except AttributeError:                    # Py 3.8 → astor
    import astor
    new_code = astor.to_source(new_tree)

DST.write_text(new_code, encoding="utf-8")
print(f"✅ layer9.py готов — вызовы {FN} раскрыты.")