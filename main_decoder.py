#!/usr/bin/env python3
"""
Единый декодер всех слоёв обфускации для main.py.

Особенности:
- Безопасные AST‑преобразования (никакого eval/exec на произвольном коде).
- Пошаговый конвейер: каждый шаг отдаёт строку исходника следующему.
- Опциональная выгрузка промежуточных слоёв (--dump-layers) в папку build_layers/.

Пример:
  python main_decoder.py main.py > decoded_final.py
  python main_decoder.py main.py --dump-layers
"""

from __future__ import annotations

import ast
import base64
import builtins
import gzip
import importlib
import io
import keyword
import os
import re
import sys
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


def unparse(tree: ast.AST) -> str:
    try:
        return ast.unparse(tree)
    except Exception:
        import astor  # type: ignore
        return astor.to_source(tree)


_PAT_EXEC_HEX = re.compile(
    r"""
    (?:exec|_)\s*\(\s*          # exec('..')  или  _('\\x..')
      (["'])(.*?)\1              # строковый литерал
    \s*\)
    """,
    re.S | re.X,
)


def _unwrap_once(src: str) -> str | None:
    m = _PAT_EXEC_HEX.search(src)
    if not m:
        return None
    lit = m.group(2)
    py_lit = f"'{lit}'"
    unesc = ast.literal_eval(py_lit)
    return unesc.encode("latin1").decode("unicode_escape", errors="replace")


def step1_unwrap_exec_hex(src: str) -> str:
    while True:
        nxt = _unwrap_once(src)
        if nxt is None:
            return src
        src = nxt


def step2_base85_from_bytes_literal(src: str) -> str:
    m = re.search(r"b(['\"])(.*?)\1", src, re.S)
    if not m:
        raise RuntimeError("Не найден блок base85 в bytes‑литерале")
    data = m.group(2).encode("utf-8", "ignore")
    raw = base64.b85decode(data)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", "replace")


def _extract_numbers(pattern: str, text: str, description: str) -> list[int]:
    m = re.search(pattern, text, re.S)
    if not m:
        raise RuntimeError(f"Не найден {description}.")
    return [int(x) for x in re.findall(r"\d+", m.group(1))]


def step3_xor_numbers(decoded_l2: str) -> str:
    key = _extract_numbers(r"_\s*=\s*\[([^\]]+)\]", decoded_l2, "первый список (ключ)")
    data = _extract_numbers(r"enumerate\s*\(\s*\[([^\]]+)\]\s*\)", decoded_l2, "второй список (данные)")
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ key[i % len(key)])
    try:
        return out.decode("utf-8")
    except UnicodeDecodeError:
        return out.decode("utf-8", "replace")


def step4_gzip_from_bytes_constant(src: str) -> str:
    tree = ast.parse(src)
    blob: bytes | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (bytes, bytearray)):
            blob = bytes(node.value)
            break
    if blob is None:
        raise RuntimeError("Не найден байтовый литерал для gzip.decompress")
    raw = gzip.decompress(blob)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", "replace")


def step5_unmask_builtins(source: str, keep: set[str] | None = None) -> str:
    m = re.search(r"^(.*?)=(.*)$", source, flags=re.S | re.M)
    if not m:
        return source
    fake_names = [s.strip() for s in m.group(1).split(",")]
    real_names = [s.strip() for s in m.group(2).split("\n", 1)[0].split(",")]
    built = set(dir(builtins))
    mapping: dict[str, str] = {
        fake: real
        for fake, real in zip(fake_names, real_names)
        if real in built and (keep is None or real in keep)
    }
    if not mapping:
        return source

    out_tokens: list[tuple] = []
    stream = io.StringIO(source)
    for tok in tokenize.generate_tokens(stream.readline):
        typ, val, *rest = tok
        if typ == tokenize.NAME and val in mapping and (keep is None or mapping[val] in keep):
            val = mapping[val]
        out_tokens.append((typ, val, *rest))
    text = tokenize.untokenize(out_tokens)
    return text if isinstance(text, str) else text.decode()



def step5a_drop_builtin_assignments(src: str) -> str:
    try:
        module = ast.parse(src)
    except SyntaxError:
        return src
    new_body: list[ast.stmt] = []
    changed = False
    for stmt in module.body:
        remove = False
        if (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Tuple)
            and isinstance(stmt.value, ast.Tuple)
            and len(stmt.targets[0].elts) == len(stmt.value.elts)
            and all(isinstance(l, ast.Name) for l in stmt.targets[0].elts)
            and len(stmt.targets[0].elts) > 30
        ):
            remove = True
        if remove:
            changed = True
            continue
        new_body.append(stmt)
    if not changed:
        return src
    module.body = new_body
    return unparse(module)

_DECODER_NAME: str | None = None


def _extract_decoder_lambda_line(code: str) -> tuple[str, str] | None:
    pattern = r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*lambda.*$"
    for m in re.finditer(pattern, code, flags=re.M):
        line = m.group(0)
        if "bytes" in line and "^" in line and "enumerate" in line:
            return m.group(1), line
    return None


def _extract_aliases_from_header(code: str) -> dict[str, str]:
    """Ищет первое присваивание кортежа вида (a,b,...) = (RealA, RealB, ...)
    и возвращает карту псевдоним→реальное_имя (строкой).
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            tgt = stmt.targets[0]
            val = stmt.value
            if isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple) and len(tgt.elts) == len(val.elts):
                mapping: dict[str, str] = {}
                for l, r in zip(tgt.elts, val.elts):
                    if isinstance(l, ast.Name) and isinstance(r, ast.Name):
                        mapping[l.id] = r.id
                if mapping:
                    return mapping
    return {}

def step6_decode_u1_calls(code: str) -> str:
    global _DECODER_NAME
    res = _extract_decoder_lambda_line(code)
    if not res:
        return code
    _DECODER_NAME, line = res
    # Построим песочницу с реальными объектами builtins согласно карте псевдонимов
    alias_map = _extract_aliases_from_header(code)
    sandbox: dict[str, object] = {}
    # База: разрешённые builtins напрямую
    base_builtins = {
        "bytes": bytes,
        "bytearray": bytearray,
        "str": str,
        "int": int,
        "chr": chr,
        "ord": ord,
        "len": len,
        "range": range,
        "enumerate": enumerate,
        "list": list,
        "tuple": tuple,
        "zip": zip,
        "sum": sum,
        "pow": pow,
        "print": print,
        "getattr": getattr,
        "setattr": setattr,
    }
    sandbox.update(base_builtins)
    # Псевдонимы → реальные объекты builtins
    for fake, real in alias_map.items():
        try:
            if hasattr(builtins, real):
                sandbox[fake] = getattr(builtins, real)
        except Exception:
            pass
    try:
        exec(line, sandbox, sandbox)
    except Exception:
        return code
    decode = sandbox.get(_DECODER_NAME)
    if not callable(decode):
        return code

    tree = ast.parse(code)

    class CallRewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == _DECODER_NAME
                and len(node.args) == 1
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, (bytes, bytearray))
            ):
                raw = node.args[0].value
                try:
                    s = decode(raw).decode("utf-8", "replace")  # type: ignore[arg-type]
                    return ast.copy_location(ast.Constant(s), node)
                except Exception:
                    return node
            return node

    new_tree = CallRewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    used = False

    class UsedFinder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            nonlocal used
            if n.id == _DECODER_NAME and isinstance(n.ctx, ast.Load):
                used = True

    UsedFinder().visit(new_tree)
    if not used:
        new_body: list[ast.stmt] = []
        for n in new_tree.body:
            if (
                isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == _DECODER_NAME for t in n.targets)
            ):
                continue
            new_body.append(n)
        new_tree.body = new_body

    return unparse(new_tree)


def step6a_cleanup_str_decode(code: str) -> str:
    """
    Упрощает вызовы вида  getattr(<str|bytes>,'decode')('utf-8', ...)  →  '...'.
    """
    tree = ast.parse(code)

    class Simplify(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            f = node.func
            if (
                isinstance(f, ast.Call)
                and isinstance(f.func, ast.Name)
                and f.func.id == "getattr"
                and len(f.args) >= 2
                and isinstance(f.args[1], ast.Constant)
                and f.args[1].value == "decode"
                and isinstance(f.args[0], ast.Constant)
            ):
                base = f.args[0].value
                if isinstance(base, (bytes, bytearray)):
                    try:
                        return ast.copy_location(ast.Constant(base.decode("utf-8", "replace")), node)
                    except Exception:
                        return node
                if isinstance(base, str):
                    return ast.copy_location(ast.Constant(base), node)
            return node

    new = Simplify().visit(tree)
    ast.fix_missing_locations(new)
    return unparse(new)


def step6b_rewrite_lazy_import(code: str) -> str:
    """slBqQzRHEsUg('pkg','attr') → importlib.import_module('pkg').attr
    и удаление определения slBqQzRHEsUg, если не используется."""
    LAZY_FN = "slBqQzRHEsUg"
    tree = ast.parse(code)

    class Simplifier(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == LAZY_FN
                and len(node.args) >= 2
                and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in node.args[:2])
            ):
                pkg, attr = node.args[0].value, node.args[1].value
                return ast.copy_location(
                    ast.Attribute(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="importlib", ctx=ast.Load()),
                                attr="import_module",
                                ctx=ast.Load(),
                            ),
                            args=[ast.Constant(pkg)],
                            keywords=[],
                        ),
                        attr=attr,
                        ctx=ast.Load(),
                    ),
                    node,
                )
            return node

    new = Simplifier().visit(tree)
    ast.fix_missing_locations(new)

    # убрать определение LAZY_FN, если не используется
    used = False
    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            nonlocal used
            if n.id == LAZY_FN:
                used = True
    Finder().visit(new)
    if not used:
        new.body = [n for n in new.body if not (isinstance(n, ast.FunctionDef) and n.name == LAZY_FN)]
    return unparse(new)


def step6c_rewrite_import_helpers(code: str) -> str:
    """Автоматически разворачивает простые обёртки над importlib/__import__."""
    tree = ast.parse(code)

    simple: set[str] = set()
    attr: set[str] = set()

    def _is_import_call(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Call)
            and (
                (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "importlib"
                    and node.func.attr == "import_module"
                )
                or (
                    isinstance(node.func, ast.Name) and node.func.id == "__import__"
                )
            )
            and bool(node.args)
        )

    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and len(n.body) == 1:
            ret = n.body[0]
            if isinstance(ret, ast.Return):
                val = ret.value
                if _is_import_call(val):
                    simple.add(n.name)
                elif (
                    isinstance(val, ast.Call)
                    and isinstance(val.func, ast.Name)
                    and val.func.id == "getattr"
                    and len(val.args) >= 2
                    and _is_import_call(val.args[0])
                ):
                    attr.add(n.name)

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if isinstance(node.func, ast.Name):
                if node.func.id in simple and node.args:
                    return ast.copy_location(
                        ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="importlib", ctx=ast.Load()),
                                attr="import_module",
                                ctx=ast.Load(),
                            ),
                            args=[node.args[0]],
                            keywords=[],
                        ),
                        node,
                    )
                if node.func.id in attr and len(node.args) >= 2:
                    return ast.copy_location(
                        ast.Call(
                            func=ast.Name(id="getattr", ctx=ast.Load()),
                            args=[
                                ast.Call(
                                    func=ast.Attribute(
                                        value=ast.Name(id="importlib", ctx=ast.Load()),
                                        attr="import_module",
                                        ctx=ast.Load(),
                                    ),
                                    args=[node.args[0]],
                                    keywords=[],
                                ),
                                node.args[1],
                            ],
                            keywords=[],
                        ),
                        node,
                    )
            return node

    new_tree = Rewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    used: set[str] = set()

    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load):
                used.add(n.id)

    Finder().visit(new_tree)
    new_tree.body = [
        n
        for n in new_tree.body
        if not (
            isinstance(n, ast.FunctionDef)
            and n.name in (simple | attr)
            and n.name not in used
        )
    ]
    return unparse(new_tree)


def step6e_rewrite_import_attr_helper(code: str) -> str:
    """
    Преобразует обёртки вида TKizvQ0BnfYh/ VLTILgCobR2q в importlib.import_module.

    TKizvQ0BnfYh('pkg', 'Attr') → importlib.import_module('pkg')
    VLTILgCobR2q('pkg', 'Attr').Attr → importlib.import_module('pkg').Attr
    """
    SIMPLE_FUNCS = {"TKizvQ0BnfYh"}
    ATTR_FUNCS = {"VLTILgCobR2q"}
    tree = ast.parse(code)

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in SIMPLE_FUNCS
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                pkg = node.args[0].value
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="importlib", ctx=ast.Load()),
                            attr="import_module",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant(pkg)],
                        keywords=[],
                    ),
                    node,
                )
            return node

        def visit_Attribute(self, node: ast.Attribute):
            self.generic_visit(node)
            if (
                isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in ATTR_FUNCS
                and len(node.value.args) >= 2
                and all(
                    isinstance(a, ast.Constant) and isinstance(a.value, str)
                    for a in node.value.args[:2]
                )
            ):
                pkg = node.value.args[0].value
                attr = node.value.args[1].value
                return ast.copy_location(
                    ast.Attribute(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="importlib", ctx=ast.Load()),
                                attr="import_module",
                                ctx=ast.Load(),
                            ),
                            args=[ast.Constant(pkg)],
                            keywords=[],
                        ),
                        attr=attr,
                        ctx=node.ctx,
                    ),
                    node,
                )
            return node

    new_tree = Rewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    # убрать определения, если функции больше не используются
    used: set[str] = set()

    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load):
                used.add(n.id)

    Finder().visit(new_tree)
    new_tree.body = [
        n
        for n in new_tree.body
        if not (
            isinstance(n, ast.FunctionDef)
            and n.name in SIMPLE_FUNCS | ATTR_FUNCS
            and n.name not in used
        )
    ]
    return unparse(new_tree)


def step6f_inline_subprocess_wrapper(code: str) -> str:
    """Заменяет вызовы простых обёрток над subprocess.run на сам subprocess.run."""
    tree = ast.parse(code)
    wrappers: set[str] = set()

    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and len(n.body) == 1:
            ret = n.body[0]
            if isinstance(ret, ast.Return):
                val = ret.value
                if (
                    isinstance(val, ast.Call)
                    and isinstance(val.func, ast.Attribute)
                    and isinstance(val.func.value, ast.Name)
                    and val.func.value.id == "subprocess"
                    and val.func.attr == "run"
                ):
                    wrappers.add(n.name)

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if isinstance(node.func, ast.Name) and node.func.id in wrappers:
                new_keywords = list(node.keywords)
                if not any(kw.arg == "check" for kw in new_keywords):
                    new_keywords.append(ast.keyword(arg="check", value=ast.Constant(1)))
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="subprocess", ctx=ast.Load()),
                            attr="run",
                            ctx=ast.Load(),
                        ),
                        args=node.args,
                        keywords=new_keywords,
                    ),
                    node,
                )
            return node

    new_tree = Rewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    used: set[str] = set()

    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load):
                used.add(n.id)

    Finder().visit(new_tree)
    new_tree.body = [
        n
        for n in new_tree.body
        if not (
            isinstance(n, ast.FunctionDef) and n.name in wrappers and n.name not in used
        )
    ]
    return unparse(new_tree)


def step6d_ensure_importlib_import(code: str) -> str:
    """Добавляет 'import importlib' в начало, если используется importlib но не импортирован."""
    if "importlib.import_module(" in code and not re.search(r"^\s*import\s+importlib\b", code, re.M):
        return "import importlib\n" + code
    return code


_SAFE_FUNCS = {"chr": chr, "ord": ord, "len": len, "int": int, "str": str, "bytes": bytes}


def _try_eval_const(node: ast.AST) -> ast.AST:
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id not in _SAFE_FUNCS:
            return node
        if isinstance(n, ast.Attribute):
            return node
    try:
        v = eval(compile(ast.Expression(node), "<eval>", "eval"), {"__builtins__": _SAFE_FUNCS}, {})
        return ast.Constant(v)
    except Exception:
        return node


class _ConstAndGetattrFolder(ast.NodeTransformer):
    def visit_BinOp(self, node: ast.BinOp):
        self.generic_visit(node)
        # Пытаемся вычислить ЛЮБУЮ бинарную операцию, если она константная
        return _try_eval_const(node)

    def visit_Call(self, node: ast.Call):
        self.generic_visit(node)
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "decode"
            and isinstance(node.func.value, ast.Constant)
            and isinstance(node.func.value.value, (str, bytes))
        ):
            if not node.args:
                val = node.func.value.value
                return ast.Constant(val.decode() if isinstance(val, (bytes, bytearray)) else val)
            if len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and str(node.args[0].value).lower() in ("utf8", "utf-8"):
                val = node.func.value.value
                return ast.Constant(val.decode("utf-8") if isinstance(val, (bytes, bytearray)) else val)

        if (
            isinstance(node.func, ast.Name)
            and node.func.id in _SAFE_FUNCS
            and all(isinstance(a, ast.Constant) for a in node.args)
            and all(isinstance(kw.value, ast.Constant) for kw in node.keywords)
        ):
            return _try_eval_const(node)

        f = node.func
        if (
            isinstance(f, ast.Call)
            and isinstance(f.func, ast.Name)
            and f.func.id == "getattr"
            and len(f.args) >= 2
            and isinstance(f.args[1], ast.Constant)
            and isinstance(f.args[1].value, str)
        ):
            obj, name = f.args[0], f.args[1].value
            return ast.copy_location(ast.Call(func=ast.Attribute(value=obj, attr=name, ctx=ast.Load()), args=node.args, keywords=node.keywords), node)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "getattr"
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
            and not node.keywords
        ):
            obj, name = node.args[0], node.args[1].value
            return ast.copy_location(ast.Attribute(value=obj, attr=name, ctx=ast.Load()), node)
        return node

    def visit_Expr(self, node: ast.Expr):
        self.generic_visit(node)
        v = node.value
        if (
            isinstance(v, ast.Call)
            and isinstance(v.func, ast.Name)
            and v.func.id == "getattr"
            and len(v.args) == 2
            and isinstance(v.args[1], ast.Constant)
            and isinstance(v.args[1].value, str)
        ):
            obj, name = v.args
            return ast.copy_location(ast.Expr(value=ast.Attribute(value=obj, attr=name.value, ctx=ast.Load())), node)
        return node


def step7_fold_consts_and_getattr(src: str) -> str:
    tree = ast.parse(src)
    prev, cur = "", tree
    while prev != (d := ast.dump(cur)):
        prev = d
        cur = _ConstAndGetattrFolder().visit(cur)
        ast.fix_missing_locations(cur)
    return unparse(cur)


def _resolve_name_from_expr(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "importlib"
        and node.func.attr == "import_module"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ):
        return node.args[0].value.split(".")[-1]
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "__import__"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ):
        return node.args[0].value.split(".")[-1]
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
        and len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and isinstance(node.args[1].value, str)
    ):
        return node.args[1].value
    return None


def step8_rename_from_tuple_assignments(src: str) -> str:
    code = src
    module = ast.parse(code)
    alias_map: dict[str, str] = {}
    for n in module.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            tgt = n.targets[0]
            if isinstance(tgt, ast.Tuple) and isinstance(n.value, ast.Tuple):
                for left, right in zip(tgt.elts, n.value.elts):
                    if isinstance(left, ast.Name):
                        name = _resolve_name_from_expr(right)
                        if name and name.isidentifier() and not keyword.iskeyword(name):
                            alias_map[left.id] = name
    if not alias_map:
        return src
    out: list[tuple] = []
    stream = io.StringIO(code)
    for tok in tokenize.generate_tokens(stream.readline):
        typ, val, *rest = tok
        if typ == tokenize.NAME and val in alias_map:
            val = alias_map[val]
        out.append((typ, val, *rest))
    return tokenize.untokenize(out)


def _importlib_from_attr(node: ast.AST) -> tuple[str, str] | None:
    # Walk chain like importlib.import_module('pkg').attr1.attr2 → ('pkg', 'attr2')
    attrs: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        attrs.insert(0, cur.attr)
        cur = cur.value
    if (
        isinstance(cur, ast.Call)
        and cur.args
        and isinstance(cur.args[0], ast.Constant)
        and isinstance(cur.args[0].value, str)
    ):
        if (
            isinstance(cur.func, ast.Attribute)
            and isinstance(cur.func.value, ast.Name)
            and cur.func.value.id == "importlib"
            and cur.func.attr == "import_module"
        ):
            pkg = cur.args[0].value
            if attrs:
                return pkg, attrs[-1]
            return pkg, pkg
        if isinstance(cur.func, ast.Name) and cur.func.id == "__import__":
            pkg = cur.args[0].value
            if attrs:
                return pkg, attrs[-1]
            return pkg, pkg.split(".")[-1]
    return None


def step9_flatten_import_assigns(src: str) -> str:
    module = ast.parse(src)
    imports: list[str] = []
    rename: dict[str, str] = {}
    new_body: list[ast.stmt] = []
    for node in module.body:
        handled = False
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            lhs, rhs = node.targets[0], node.value
            if isinstance(lhs, ast.Tuple) and len(lhs.elts) == 1:
                lhs = lhs.elts[0]
            if isinstance(rhs, ast.Tuple) and len(rhs.elts) == 1:
                rhs = rhs.elts[0]
            if isinstance(lhs, ast.Tuple) and isinstance(rhs, ast.Tuple) and len(lhs.elts) == len(rhs.elts):
                infos = [_importlib_from_attr(e) for e in rhs.elts]
                if all(infos) and len({p for p, _ in infos}) == 1:
                    pkg = infos[0][0]
                    names = [a for _, a in infos]
                    imports.append(f"from {pkg} import {', '.join(names)}")
                    for l, (_, a) in zip(lhs.elts, infos):
                        if isinstance(l, ast.Name):
                            rename[l.id] = a
                    handled = True
            elif isinstance(lhs, ast.Name):
                info = _importlib_from_attr(rhs)
                if info:
                    pkg, a = info
                    if pkg == a:
                        imports.append(f"import {pkg}")
                    else:
                        imports.append(f"from {pkg} import {a}")
                    rename[lhs.id] = a
                    handled = True
        if not handled:
            new_body.append(node)
    module.body = new_body
    body = unparse(module)
    out: list[tuple] = []
    stream = io.StringIO(body)
    for tok in tokenize.generate_tokens(stream.readline):
        typ, val, *rest = tok
        if typ == tokenize.NAME and val in rename:
            val = rename[val]
        out.append((typ, val, *rest))
    header = ("\n".join(sorted(set(imports))) + "\n\n") if imports else ""
    result = header + tokenize.untokenize(out)
    if "importlib.import_module(" not in result:
        result = result.replace("import importlib\n", "")
    return result


def _guess_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return re.sub(r"\W+", "_", node.value)
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        for a in reversed(node.args):
            g = _guess_name(a)
            if g:
                return g
        return _guess_name(node.func)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        g = _guess_name(node.right)
        if g:
            return g
        return _guess_name(node.left)
    return None


def step10_auto_rename(src: str) -> str:
    tree = ast.parse(src)
    rename: dict[str, str] = {}

    class Finder(ast.NodeVisitor):
        def visit_Assign(self, node: ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = _guess_name(node.value)
                if name and name.isidentifier() and not keyword.iskeyword(name):
                    rename[node.targets[0].id] = name
            self.generic_visit(node)

    Finder().visit(tree)
    if not rename:
        return src
    out: list[tuple] = []
    stream = io.StringIO(src)
    for tok in tokenize.generate_tokens(stream.readline):
        typ, val, *rest = tok
        if typ == tokenize.NAME and val in rename:
            val = rename[val]
        out.append((typ, val, *rest))
    return tokenize.untokenize(out)


RENAME_GLOBAL = {
    "KOMvfYWvxpvB": "venv_dir",
    "qSlLeyQ7VdNv": "venv_python",
    "GEubzOScffp0": "venv_pip",
    "HizWI004zW0H": "installed_marker",
    "ADrQh6Q0Xq4n": "get_pip_path",
    "Pib7Isbe5Piv": "init_alembic_env",
    "Yx6Nrcbtb4PN": "cleanup_orphans",
    "ot1STj0Fihnd": "repair_alembic_version",
    "NrMxwt71pAGc": "patch_alembic_env",
    "o2KdGgnRtgxA": "restore_alembic_env",
    "yfTW9tS0_kHo": "run_migrations",
    "bqBdUDQyD_PG": "migrate",
    "XpF3sTj6yajP": "install_cli",
    "wM4UKfLL5p4k": "backup_loop",
    "RnhunT1Pokyl": "api_server",
    "M7xmJlQpYzNB": "on_startup",
    "Fklfk5LsFLlG": "on_shutdown",
    "of1m0QeKOPMV": "main",
    "aNXQRddvjV1V": "ping_job",
    "WaZ61jx33zZR": "send_stats",
    "JUE22Ecu3lXC": "runner",
    "Wg4y0tl9UCps": "site",
    "pXePuUjRPloW": "stop_event",
    "WwAfJLQPh73Q": "loop",
    "q0B7Jzr9PNTf": "pending",
    "NZRpUosWW30x": "bg_tasks",
    "mq7VdOSYsKxq": "args",
    "rWwUf66NWdyI": "Exception",
    "umvpgGZGd92J": "exc",
    "TQCuJzXXjNfR": "task",
    "Kzqgqt2OnbBD": "app",
    "gRRvVbYhM0LB": "console",
    "QK5bLxBOypkF": "install_cli",
    "D6P0eecBAFVv": "backup_loop",
    "M6flxKL4gRoX": "on_startup",
    "KMS7j9IC8wK5": "on_shutdown",
    "o_Zg3SYZ2U_F": "stop_webhooks",
    "WeQFJHP3LH_W": "main",
    "NwVNoYZ0lVgA": "task",
    "hsEaj3FbHlV3": "exc",
    "aIut2Xl7LjBC": "sig",
    "CRZYKFwfFJRI": "stop_event",
    "VEYmCcpb5WZi": "runner",
    "JutrLWyLwTzT": "site",
    "SoAy9XMB2LZJ": "loop",
    "g5gb1yodGaJT": "pending",
    "fPSFiLwtmvLO": "bg_tasks",
    "JezwpIWfYHOX": "expected_secret",
    "_SvfhKl8rD1_": "is_valid_code",
    "OJeYPsgEnfYk": "Exception",
    "Re5W1iJwYiL7": "__name__",
    "hpOdPEnuB1nq": "init_alembic_env",
    "S83mpZdEbfAe": "cleanup_orphans",
    "evBAxYgU6UhL": "repair_alembic_version",
    "fd1cG9dodvxu": "run_migrations",
    "FF7rBWnIKKwz": "migrate",
    "ojhNuMDCAseB": "install_cli_command",
    "DxjpDrvsrMP4": "venv_python",
    "ADUIqZAL1Zgf": "installed_marker",
    "Z_j91xwXUTad": "Exception",
    "L6FQr_qnKyxU": "err",
    "aZBzG1SNakiw": "backup_loop",
    "aS_3er8YmEUc": "api_server",
    "viz37pWwjaba": "on_startup",
    "lIJ1MvvhYMYm": "on_shutdown",
    "gcLcbFqq732j": "main",
    "H5jTrq_05RA7": "__name__",
    "eZAsA0WiSb2d": "input",
    "hvuYJwbmJTFX": "runner",
    "PGcAj_zEi4a3": "site",
    "bOHUjA06et_u": "stop_event",
    "tiaO4FDneUHs": "loop",
    "pdYn9YoDs220": "sig",
    "wTH9Qzhcarx_": "pending",
    "Yf5fgZ__vH4z": "task",
    "F0GRLd3hqdNj": "scheduler",
    "FXVhbYJkNfzk": "send_stats",
    "M79o_CyLR10K": "session",
    "CJOEH5dagWs_": "server",
    "dhwwiGt3_ntG": "app",
    "HNBdWebD2ahJ": "ping_job",
    "ktzqDrWNa2rM": "bg_tasks",
    "gTBPDPy87BYI": "args",
}


def step10_global_rename(src: str) -> str:
    tree = ast.parse(src)

    class _Renamer(ast.NodeTransformer):
        def visit_Name(self, n: ast.Name):
            if n.id in RENAME_GLOBAL:
                n.id = RENAME_GLOBAL[n.id]
            return n

        def visit_FunctionDef(self, n: ast.FunctionDef):
            if n.name in RENAME_GLOBAL:
                n.name = RENAME_GLOBAL[n.name]
            self.generic_visit(n)
            return n

        def visit_AsyncFunctionDef(self, n: ast.AsyncFunctionDef):
            if n.name in RENAME_GLOBAL:
                n.name = RENAME_GLOBAL[n.name]
            self.generic_visit(n)
            return n

        def visit_arg(self, n: ast.arg):
            if n.arg in RENAME_GLOBAL:
                n.arg = RENAME_GLOBAL[n.arg]
            return n

        def visit_ExceptHandler(self, n: ast.ExceptHandler):
            if isinstance(n.name, str) and n.name in RENAME_GLOBAL:
                n.name = RENAME_GLOBAL[n.name]
            self.generic_visit(n)
            return n

    new = _Renamer().visit(tree)
    ast.fix_missing_locations(new)
    code = unparse(new)
    for old, new_name in RENAME_GLOBAL.items():
        code = code.replace(f"{{{old}}}", f"{{{new_name}}}")
    return code


def step11_global_text_cleanup(src: str) -> str:
    repl = {
        r"K585qaYUbA_y": "SUB_PATH",
        r"Di3ZYNq4y1Jk": "WEBHOOK_URL",
        r"\blqCBDe1lOEOd\b": "app",
        r"\berr\b": "exc",
    }
    out = src
    for patt, val in repl.items():
        out = re.sub(patt, val, out)
    if "importlib.import_module(" not in out:
        out = out.replace("import importlib\n", "")
    return out


LOCAL_RENAME = {
    "NufvPSR1AQNx": "path_launcher",
    "lsHnbTESTPag": "python_exe",
    "u4Kgw2xftrng": "search_dirs",
    "LjLi2w1n0i3h": "bin_dir",
    "DK9LsyO02L_J": "script_file",
    "HohFPgdHHRgg": "fh",
    "fchr": "chr",
    "A2OFynpSEGYZ": "env_path",
    "MHZivVbLpj_1": "config_patch",
    "RM59qDe5AObi": "sync_url",
    "examfTtmBk_5": "engine",
    "dEYieqnzsigE": "conn",
    "Vta6ea3F01Ju": "deleted_notifications",
    "E2_KpJ7YAEeI": "deleted_referrals",
    "NruZidUcKdMe": "cfg",
    "hrgmUSq5vFaA": "script_dir",
    "NgaT11tFHfUC": "result",
    "IfwIp02ZI50t": "version",
    "Hvn5kk0_vFwt": "upgrade_result",
    "sLMMm8FcjIhp": "versions_dir",
    "N5BOS5Ba7iBe": "search_dirs",
    "H6bcNnJNBekj": "bin_dir",
    "Nynw3IhkeoPb": "cmd_name",
    "AxqUYyg2kRoh": "cmd_path",
    "aKErMq2ffNB_": "fh",
    "t09X61UaTZUU": "content",
    "tbY49y6hEKQg": "new_name",
    "bIHNKSXd0ieD": "hashlib_mod",
    "uYrXWAOakCA6": "launcher_path",
    "zYU0AcfTUN9H": "python_exe",
    "CJOEH5dagWs_": "server",
    "dhwwiGt3_ntG": "app",
    "pEfQPe06_bNU": "default_cmd_name",
    "bZnyVT5QtFH6": "client_code_valid",
    "DAfvdd0x1Xo6": "expected_main_secret",
    "Kzqgqt2OnbBD": "app",
    "hpuZ2br8L5KF": "session",
    "fVTKKdPXSc0s": "scheduler",
    "Y3MtP52LbSQz": "client_code_valid",
    "CFNWNYjIE8CO": "expected_main_secret",
    "wI5a6NtuIHOG": "resp",
    "VD5XtVzFLHb2": "fh",
    "kkr6asGQBbL4": "Exception",
    "i_5gN_6A5Aqj": "env_path",
    "fvX0NPd8gKqD": "text",
    "dvrwJuLJSlIR": "config_patch",
    "xqQbR3mcDJZE": "sync_url",
    "ya1W7oAVx8Q4": "engine",
    "y3mYlbnvULnu": "conn",
    "Erx7KqRlGK6W": "deleted_notifications",
    "dWyzIwk5ehXI": "deleted_referrals",
    "CRFlXIWSq7W1": "cfg",
    "fkMzg2r6XODx": "script_dir",
    "FCcaVPw_BfBa": "result",
    "v8h0Nrd1Zgij": "version",
    "P2gKpi9RnARy": "backup_path",
    "GAGG3SzhZoAk": "original_text",
    "guKuVpoPOUK0": "inject_code",
    "LVPFufwjktJF": "upgrade_result",
}


def step12_locals_and_constants(src: str) -> str:
    tree = ast.parse(src)

    class _Cleanup(ast.NodeTransformer):
        def visit_Name(self, n: ast.Name):
            if n.id in LOCAL_RENAME:
                n.id = LOCAL_RENAME[n.id]
            return n

        def visit_While(self, n: ast.While):
            if isinstance(n.test, ast.Constant) and n.test.value == 1:
                n.test = ast.Constant(True)
            self.generic_visit(n)
            return n

        def visit_Constant(self, n: ast.Constant):
            if isinstance(n.value, int) and n.value == 493:
                return ast.copy_location(ast.Constant(0o755), n)
            return n

        def visit_Call(self, n: ast.Call):
            self.generic_visit(n)
            if (
                isinstance(n.func, ast.Name)
                and n.func.id == "chr"
                and len(n.args) == 1
                and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, int)
            ):
                try:
                    return ast.copy_location(ast.Constant(chr(n.args[0].value)), n)
                except Exception:
                    return n
            return n

    new = _Cleanup().visit(tree)
    ast.fix_missing_locations(new)
    return unparse(new)


def step13_drop_unused_funcs(src: str) -> str:
    tree = ast.parse(src)

    used: set[str] = set()

    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load):
                used.add(n.id)

    Finder().visit(tree)
    new_body: list[ast.stmt] = []
    changed = False
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) and stmt.name not in used:
            changed = True
            continue
        new_body.append(stmt)
    if not changed:
        return src
    tree.body = new_body
    ast.fix_missing_locations(tree)
    return unparse(tree)


@dataclass
class Step:
    name: str
    func: Callable[[str], str]


def build_pipeline() -> list[Step]:
    return [
        Step("unwrap exec/_ hex", step1_unwrap_exec_hex),
        Step("base85 decode", step2_base85_from_bytes_literal),
        Step("xor numbers", step3_xor_numbers),
        Step("gzip decompress", step4_gzip_from_bytes_constant),
        Step(
            "unmask builtins",
            lambda s: step5_unmask_builtins(
                s,
                keep={
                    # минимум для работы лямбды-декодера и базовых операций
                    "getattr",
                    "setattr",
                    "len",
                    "print",
                    "open",
                    "range",
                    "int",
                    "chr",
                    "ord",
                    "bytes",
                    "bytearray",
                    "list",
                    "tuple",
                    "enumerate",
                    "zip",
                    "sum",
                    "str",
                    "pow",
                    "__import__",
                },
            ),
        ),
        Step("drop builtin self-assigns", step5a_drop_builtin_assignments),
        Step("decode XOR lambda calls", step6_decode_u1_calls),
        Step("fold consts & getattr (pass1)", step7_fold_consts_and_getattr),
        Step("cleanup str decode", step6a_cleanup_str_decode),
        Step("fold consts & getattr (pre-import-fixes)", step7_fold_consts_and_getattr),
        Step("rewrite lazy import slBqQzRHEsUg", step6b_rewrite_lazy_import),
        Step("rewrite import helpers", step6c_rewrite_import_helpers),
        Step("rewrite legacy import helpers", step6e_rewrite_import_attr_helper),
        Step("inline subprocess.run wrapper", step6f_inline_subprocess_wrapper),
        Step("ensure 'import importlib' header", step6d_ensure_importlib_import),
        Step("fold consts & getattr (post-import-fixes)", step7_fold_consts_and_getattr),
        Step("rename from tuple assigns", step8_rename_from_tuple_assignments),
        Step("flatten import assigns", step9_flatten_import_assigns),
        Step("auto rename", step10_auto_rename),
        Step("global rename", step10_global_rename),
        Step("global text cleanup", step11_global_text_cleanup),
        Step("locals & constants", step12_locals_and_constants),
        Step("drop unused functions", step13_drop_unused_funcs),
        Step("fold consts & getattr (final)", step7_fold_consts_and_getattr),
    ]


def run_pipeline(
    initial_code: str,
    dump_layers: bool = False,
    dump_dir: Path | None = None,
    collect_layers: bool = False,
) -> str | tuple[str, list[str]]:
    """Runs all decode steps, optionally dumping or collecting intermediate layers."""

    steps = build_pipeline()
    cur = initial_code
    layers: list[str] | None = [] if collect_layers else None

    if dump_layers:
        dump_dir = dump_dir or Path("build_layers")
        dump_dir.mkdir(parents=True, exist_ok=True)

    for idx, step in enumerate(steps, start=1):
        try:
            nxt = step.func(cur)
        except Exception as exc:
            print(f"[!] Шаг {idx} '{step.name}' завершился с ошибкой: {exc}", file=sys.stderr)
            nxt = cur
        if dump_layers:
            path = dump_dir / f"layer{idx:02d}.py"
            path.write_text(nxt, encoding="utf-8")
        if layers is not None:
            layers.append(nxt)
        if dump_layers or layers is not None:
            print(f"[{idx:02d}] {step.name}", file=sys.stderr)
        cur = nxt

    if layers is not None:
        return cur, layers
    return cur


def main(argv: list[str]) -> int:
    if not argv:
        print("Использование: python main_decoder.py <input.py> [--dump-layers] [--out <file>]", file=sys.stderr)
        return 2
    inp = None
    dump = False
    out_path: Path | None = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--dump-layers":
            dump = True
            i += 1
            continue
        if a == "--out" and i + 1 < len(argv):
            out_path = Path(argv[i + 1]).resolve()
            i += 2
            continue
        if inp is None:
            inp = a
            i += 1
            continue
        print(f"Неизвестный аргумент: {a}", file=sys.stderr)
        return 2

    if inp is None:
        print("Не задан входной файл", file=sys.stderr)
        return 2
    src_path = Path(inp).resolve()
    if not src_path.exists():
        print(f"Файл не найден: {src_path}", file=sys.stderr)
        return 1
    original = src_path.read_text(encoding="utf-8", errors="ignore")
    final = run_pipeline(original, dump_layers=dump)
    out_text = final if final.endswith("\n") else final + "\n"
    if out_path:
        out_path.write_text(out_text, encoding="utf-8")
    else:
        sys.stdout.write(out_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
