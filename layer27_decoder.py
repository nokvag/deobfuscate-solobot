#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
layer28_cleanup.py
  • меняет K585qaYUbA_y → SUB_PATH
          Di3ZYNq4y1Jk → WEBHOOK_URL
          err          → exc
    не только в коде, но и ВНУТРИ f-строк/обычных строк.
  • превращает присваивания вида
        obj = (importlib.import_module('pkg.mod').obj.pkg.mod.obj,)
    в   from pkg.mod import obj
  • сохраняет результат в layer28.py
"""
from __future__ import annotations
import ast, pathlib, re, textwrap

SRC = pathlib.Path("layer27.py")
DST = pathlib.Path("layer28.py")
code = SRC.read_text("utf-8")

# ---------- 1. нормализуем импорт-кортежи -----------------------------
def convert_imports(src: str) -> tuple[str, list[str]]:
    "возвратит (исправленный_код, список_строк_импорта)"
    tree = ast.parse(src, SRC.name)
    imports: list[str] = []
    new_body: list[ast.stmt] = []

    def imp_info(node: ast.AST):
        if not isinstance(node, ast.Attribute): return None
        attr = node.attr
        base = node.value
        if isinstance(base, ast.Attribute) and base.attr == attr:
            base = base.value           # .attr.attr
        if (isinstance(base, ast.Call)
                and isinstance(base.func, ast.Attribute)
                and isinstance(base.func.value, ast.Name)
                and base.func.value.id == "importlib"
                and base.func.attr == "import_module"
                and base.args
                and isinstance(base.args[0], ast.Constant)
                and isinstance(base.args[0].value, str)):
            return base.args[0].value, attr
        return None

    for n in tree.body:
        handled = False
        if (isinstance(n, ast.Assign) and len(n.targets) == 1):
            tgt, val = n.targets[0], n.value
            # снять ( … ,)
            if isinstance(val, ast.Tuple) and len(val.elts) == 1:
                val = val.elts[0]
            if isinstance(tgt, ast.Name):
                info = imp_info(val)
                if info:
                    pkg, attr = info
                    imports.append(f"from {pkg} import {attr}")
                    handled = True
            elif isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple) \
                    and len(tgt.elts) == len(val.elts):
                infos = [imp_info(e) for e in val.elts]
                if all(infos) and len({p for p, _ in infos}) == 1:
                    pkg = infos[0][0]
                    names = [a for _, a in infos]
                    imports.append(f"from {pkg} import {', '.join(names)}")
                    handled = True
        if not handled:
            new_body.append(n)
    tree.body = new_body
    try:
        body_code = ast.unparse(tree)
    except AttributeError:
        import astor; body_code = astor.to_source(tree)
    return body_code, imports

body, imp_lines = convert_imports(code)

# ---------- 2. глобальная замена (код И строки) -----------------------
REPL = {
    "K585qaYUbA_y": "SUB_PATH",
    "Di3ZYNq4y1Jk": "WEBHOOK_URL",
    # заменяем err→exc только если слово err «отдельное»
    r"\berr\b":     "exc",
}

for patt, repl in REPL.items():
    body = re.sub(patt, repl, body)

# ---------- 3. собираем финал -----------------------------------------
header = "\n".join(sorted(set(imp_lines)))
if "import importlib" in body and not re.search(r"\bimportlib\.", body):
    # importlib теперь не нужен
    body = body.replace("import importlib\n", "")
full = (header + "\n" + body).lstrip()

DST.write_text(full, "utf-8")
print("✅ layer28.py сохранён — псевдонимы и кортеж-импорты убраны.")