#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer22_import_cleanup.py
  1. Превращает громоздкие присваивания вида
       (x, y) = (importlib.import_module('pkg').x.pkg.x,
                 importlib.import_module('pkg').y.pkg.y)
     в   from pkg import x, y
  2. Для одиночных:
       bot = importlib.import_module('bot').bot.bot
     →   from bot import bot
  3. Заменяет остаточные имена:
       K585qaYUbA_y → SUB_PATH
       lqCBDe1lOEOd → app
       Di3ZYNq4y1Jk → hook_url
       hsEaj3FbHlV3 → exc
  4. Записывает результат в layer22.py
"""
from __future__ import annotations
import ast, keyword, pathlib, tokenize, io, textwrap

SRC = pathlib.Path("layer21.py")
DST = pathlib.Path("layer22.py")

code = SRC.read_text("utf-8")
module = ast.parse(code, SRC.name)

# ---------------- helpers ----------------
def unpack_attr_chain(node: ast.Attribute) -> tuple[str, str] | None:
    """
    importlib.import_module('pkg.sub').attr(.attr)
    возвр: ('pkg.sub', 'attr')
    """
    if not isinstance(node, ast.Attribute):
        return None
    attr = node.attr
    parent = node.value
    # убираем .attr.attr повтор
    if isinstance(parent, ast.Attribute) and parent.attr == attr:
        parent = parent.value
    if (isinstance(parent, ast.Call)
            and isinstance(parent.func, ast.Attribute)
            and isinstance(parent.func.value, ast.Name)
            and parent.func.value.id == "importlib"
            and parent.func.attr == "import_module"
            and parent.args
            and isinstance(parent.args[0], ast.Constant)
            and isinstance(parent.args[0].value, str)):
        return parent.args[0].value, attr
    return None

imports: list[str] = []      # строки импорта
replacements: dict[str, str] = {}   # старое имя -> новое

new_body: list[ast.stmt] = []

for node in module.body:
    if (isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], (ast.Name, ast.Tuple))):
        targets = node.targets[0]
        value = node.value
        # если обе стороны кортежи одинаковой длины
        if isinstance(targets, ast.Tuple) and isinstance(value, ast.Tuple) \
                and len(targets.elts) == len(value.elts):
            group_ok = True
            collected = []
            for right in value.elts:
                if isinstance(right, ast.Attribute):
                    data = unpack_attr_chain(right)
                    if data:
                        collected.append(data)
                    else:
                        group_ok = False
                        break
                else:
                    group_ok = False
                    break
            if group_ok:
                # строим from pkg import a, b ...
                pkgs = {pkg for pkg, _ in collected}
                if len(pkgs) == 1:
                    pkg = pkgs.pop()
                    names = [attr for _, attr in collected]
                    imports.append(f"from {pkg} import {', '.join(names)}")
                    for tgt, (_, attr) in zip(targets.elts, collected):
                        if isinstance(tgt, ast.Name):
                            replacements[tgt.id] = attr
                    continue   # не добавляем старый Assign
        # одиночное назначение
        if isinstance(targets, ast.Name):
            if isinstance(value, ast.Attribute):
                data = unpack_attr_chain(value)
                if data:
                    pkg, attr = data
                    imports.append(f"from {pkg} import {attr}")
                    replacements[targets.id] = attr
                    continue
    new_body.append(node)

module.body = new_body

# ---------- сериализуем ----------
try:
    body_code = ast.unparse(module)
except AttributeError:
    import astor; body_code = astor.to_source(module)

# ---------- глобальные переименования ----------
replacements.update({
    "K585qaYUbA_y": "SUB_PATH",
    "lqCBDe1lOEOd": "app",
    "Di3ZYNq4y1Jk": "hook_url",
    "hsEaj3FbHlV3": "exc",
})

tok_out = []
stream = io.StringIO(body_code)
for tok in tokenize.generate_tokens(stream.readline):
    ttype, tstr, *rest = tok
    if ttype == tokenize.NAME and tstr in replacements:
        tstr = replacements[tstr]
    tok_out.append((ttype, tstr, *rest))

header = "\n".join(sorted(set(imports))) + "\n\n"
DST.write_text(header + tokenize.untokenize(tok_out), "utf-8")
print(f"✅ layer22.py создан: импорты распрямлены, имена исправлены.")