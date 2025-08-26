#!/usr/bin/env python3
# layer31_cleanup.py
"""
▪ превращает все присваивания вида
      (a, b) = (importlib.import_module('pkg.mod').a.…a,
                importlib.import_module('pkg.mod').b.…b)
      x = (importlib.import_module('pkg.mod').x.…x,)
  в   from pkg.mod import a, b, x
▪ удаляет строку «import importlib», если он больше не используется
"""

from __future__ import annotations
import ast
import io
import pathlib
import tokenize

HERE = pathlib.Path(__file__).resolve().parent
SRC  = HERE / "layer30.py"
DST  = HERE / "layer31.py"

# ---------------------------------------------------------------------
def split_import(node: ast.AST) -> tuple[str, str] | None:
    """
    Переварить цепочку Attribute-ов и вытащить
      importlib.import_module('pkg.sub').attr(.[…])*  →  ('pkg.sub', 'attr')
    """
    if not isinstance(node, ast.Attribute):
        return None
    last_attr = node.attr
    base = node.value
    # пройти вниз пока есть Attribute
    while isinstance(base, ast.Attribute):
        last_attr = base.attr
        base = base.value
    if (
        isinstance(base, ast.Call)
        and isinstance(base.func, ast.Attribute)
        and isinstance(base.func.value, ast.Name)
        and base.func.value.id == "importlib"
        and base.func.attr == "import_module"
        and base.args
        and isinstance(base.args[0], ast.Constant)
        and isinstance(base.args[0].value, str)
    ):
        return base.args[0].value, last_attr
    return None


def extract_from_assign(assign: ast.Assign):
    """Вернёт список строк-импортов или None, если не наш паттерн."""
    tgt = assign.targets[0]
    rhs = assign.value

    # снять одноэлементный кортеж справа
    if isinstance(rhs, ast.Tuple) and len(rhs.elts) == 1:
        rhs = rhs.elts[0]

    # x =  importlib…
    if isinstance(tgt, ast.Name):
        info = split_import(rhs)
        if info:
            pkg, name = info
            return [f"from {pkg} import {name}"]

    # (a, b, …) = (importlib…, importlib…)
    if isinstance(tgt, ast.Tuple) and isinstance(rhs, ast.Tuple) \
            and len(tgt.elts) == len(rhs.elts):
        infos = [split_import(e) for e in rhs.elts]
        if all(infos) and len({p for p, _ in infos}) == 1:
            pkg = infos[0][0]
            names = ", ".join(a for _, a in infos)
            return [f"from {pkg} import {names}"]
    return None


# ---------------------------------------------------------------------
src_code = SRC.read_text("utf-8")
module   = ast.parse(src_code, filename="layer30.py")

new_body: list[ast.stmt] = []
import_lines: list[str]  = []

for stmt in module.body:
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
        lines = extract_from_assign(stmt)
        if lines:               # наш «обфусцированный» импорт
            import_lines.extend(lines)
            continue            # строку-Assign выбрасываем
    new_body.append(stmt)

module.body = new_body

# сериализуем обратно
try:
    clean_code = ast.unparse(module)          # Python 3.9+
except AttributeError:
    import astor
    clean_code = astor.to_source(module)

# убираем лишний import importlib, если остатков нет
if "importlib.import_module(" not in clean_code:
    clean_code = clean_code.replace("import importlib\n", "")

final_source = (
    ("\n".join(sorted(set(import_lines))) + "\n\n") if import_lines else ""
) + clean_code.lstrip()

DST.write_text(final_source, "utf-8")
print("✅  layer31.py — все остаточные importlib-кортежи устранены")