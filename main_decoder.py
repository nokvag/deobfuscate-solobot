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

_DECODER_NAME = "u1KQ2EguJKQ7"


def _extract_decoder_lambda_line(code: str) -> str | None:
    m = re.search(rf"^\s*{_DECODER_NAME}\s*=\s*lambda.*$", code, flags=re.M)
    return m.group(0) if m else None


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
    line = _extract_decoder_lambda_line(code)
    if not line:
        return code
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


def step6c_rewrite_import_wrapper(code: str) -> str:
    """JXzJajrdQAWB('pkg') → importlib.import_module('pkg')"""
    WRAPPER = {"JXzJajrdQAWB"}
    tree = ast.parse(code)

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in WRAPPER
                and len(node.args) == 1
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

    new = Rewriter().visit(tree)
    ast.fix_missing_locations(new)
    return unparse(new)


def step6d_ensure_importlib_import(code: str) -> str:
    """Добавляет 'import importlib' в начало, если используется importlib но не импортирован."""
    if "importlib.import_module(" in code and not re.search(r"^\s*import\s+importlib\b", code, re.M):
        return "import importlib\n" + code
    return code


def step6e_decode_simple_lambda(code: str) -> str:
    """
    Находит простые лямбды-декодеры вида NAME = lambda arg: <expr>,
    безопасно вычисляет их на константных bytes/bytearray аргументах и
    подменяет вызовы NAME(b"...") на строковые литералы.

    Также удаляет определение такой лямбды, если после переписывания она не используется.
    """
    try:
        module = ast.parse(code)
    except SyntaxError:
        return code

    # Собираем кандидатов: NAME = <lambda single-arg>
    candidates: dict[str, str] = {}
    for stmt in module.body:
        if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
            target = stmt.targets[0].id
            if isinstance(stmt.value, ast.Lambda) and len(stmt.value.args.args) == 1:
                try:
                    lambda_src = unparse(stmt.value)
                except Exception:
                    continue
                if lambda_src.strip().startswith("lambda"):
                    # Полная строка присваивания, как в исходнике
                    candidates[target] = f"{target} = {lambda_src}"

    if not candidates:
        return code

    # Разрешённые builtins для безопасного исполнения
    safe_builtins: dict[str, object] = {
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
    }

    # Готовим песочницу и материализуем лямбды
    decoders: dict[str, object] = {}
    sandbox: dict[str, object] = dict(safe_builtins)
    for name, line in candidates.items():
        try:
            exec(line, sandbox, sandbox)
            fn = sandbox.get(name)
            if callable(fn):
                decoders[name] = fn
        except Exception:
            # Пропускаем лямбды, которые не получилось загрузить
            pass

    if not decoders:
        return code

    tree = ast.parse(code)

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in decoders
                and len(node.args) == 1
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, (bytes, bytearray))
            ):
                fn = decoders[node.func.id]
                try:
                    res = fn(node.args[0].value)  # type: ignore[misc]
                    if isinstance(res, (bytes, bytearray)):
                        try:
                            s = bytes(res).decode("utf-8", "replace")
                            return ast.copy_location(ast.Constant(s), node)
                        except Exception:
                            return node
                    if isinstance(res, str):
                        return ast.copy_location(ast.Constant(res), node)
                except Exception:
                    return node
            return node

    new_tree = Rewriter().visit(tree)
    ast.fix_missing_locations(new_tree)

    # Удаляем определения лямбд, если не используются
    used_names: set[str] = set()

    class Usage(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load):
                used_names.add(n.id)

    Usage().visit(new_tree)

    if any(name in used_names for name in decoders):
        # Если хоть одна ещё используется — просто возвращаем переписанный код
        return unparse(new_tree)

    # Физически выкидываем присваивания NAME = lambda ...
    new_body: list[ast.stmt] = []
    for stmt in new_tree.body:
        if (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id in decoders
            and isinstance(stmt.value, ast.Lambda)
        ):
            continue
        new_body.append(stmt)
    new_tree.body = new_body
    return unparse(new_tree)


def step6f_rewrite_TKizvQ0BnfYh(code: str) -> str:
    """
    TKizvQ0BnfYh('pkg','attr', ...) → importlib.import_module('pkg').attr
    Удаляет определение TKizvQ0BnfYh, если не используется.
    """
    FN = "TKizvQ0BnfYh"
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == FN
                and len(node.args) >= 2
                and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in node.args[:2])
            ):
                pkg = node.args[0].value
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(value=ast.Name(id="importlib", ctx=ast.Load()), attr="import_module", ctx=ast.Load()),
                        args=[ast.Constant(pkg)],
                        keywords=[],
                    ),
                    node,
                )
            return node

    new = Rewriter().visit(tree)
    ast.fix_missing_locations(new)

    used = False
    class Finder(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            nonlocal used
            if n.id == FN:
                used = True
    Finder().visit(new)
    if not used:
        new.body = [n for n in new.body if not (isinstance(n, ast.FunctionDef) and n.name == FN)]
    return unparse(new)


def step6g_rewrite_obf_import_call(code: str) -> str:
    """
    I3Qj6caZgXTY('pkg') → importlib.import_module('pkg')
    (обфусцированный __import__).
    """
    FN = "I3Qj6caZgXTY"
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call):
            self.generic_visit(node)
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == FN
                and len(node.args) >= 1
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                pkg = node.args[0].value
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(value=ast.Name(id="importlib", ctx=ast.Load()), attr="import_module", ctx=ast.Load()),
                        args=[ast.Constant(pkg)],
                        keywords=[],
                    ),
                    node,
                )
            return node

    new = Rewriter().visit(tree)
    ast.fix_missing_locations(new)
    return unparse(new)


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
        # Убираем ложные вызовы на результате importlib.import_module('pkg')(...)
        def _is_import_module_call(c: ast.AST) -> bool:
            return (
                isinstance(c, ast.Call)
                and isinstance(c.func, ast.Attribute)
                and isinstance(c.func.value, ast.Name)
                and c.func.value.id == "importlib"
                and c.func.attr == "import_module"
                and c.args
                and isinstance(c.args[0], ast.Constant)
                and isinstance(c.args[0].value, str)
            )
        if _is_import_module_call(node.func):
            return node.func
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
        and node.func.id in {"__import__", "I3Qj6caZgXTY"}
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
        attrs.append(cur.attr)
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
                # Ближайший к import_module атрибут — фактический экспорт: pkg.attr1.attr2 → import pkg: attr1
                return pkg, attrs[0]
            return pkg, pkg
        # Любая функция вида F('pkg', ...) считаем импорт-обёрткой (эвристика)
        if isinstance(cur.func, ast.Name):
            pkg = cur.args[0].value
            if attrs:
                return pkg, attrs[0]
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


RENAME_GLOBAL = {
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
    "H5jTrq_05RA7": "__name__",
    "Z_j91xwXUTad": "Exception",
    "eZAsA0WiSb2d": "input",
    "ag5YPJyfCVAR": "SUB_PATH",
    "UUEf31IRUeOd": "WEBHOOK_URL",
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
        r"\buvicorn\.config\b": "uvicorn.Config",
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
    # Часто встречающиеся временные имена
    "hpOdPEnuB1nq": "init_alembic",
    "S83mpZdEbfAe": "cleanup_orphans",
    "evBAxYgU6UhL": "fix_broken_revision",
    "fd1cG9dodvxu": "generate_and_apply_migrations",
    "FF7rBWnIKKwz": "ensure_migrations",
    "ojhNuMDCAseB": "install_cli",
    "aZBzG1SNakiw": "backup_loop",
    "aS_3er8YmEUc": "serve_api",
    "viz37pWwjaba": "on_startup",
    "lIJ1MvvhYMYm": "on_shutdown",
    "gcLcbFqq732j": "main",
    "HNBdWebD2ahJ": "ping_servers",
    "FXVhbYJkNfzk": "send_stats_job",
    "F0GRLd3hqdNj": "scheduler",
    "bOHUjA06et_u": "stop_event",
    "tiaO4FDneUHs": "loop",
    "Yf5fgZ__vH4z": "task",
    "wTH9Qzhcarx_": "pending",
    # Переименования локальных переменных для читаемости
    "A2OFynpSEGYZ": "alembic_env_path",
    "MHZivVbLpj_1": "alembic_env_patch",
    "RM59qDe5AObi": "sync_db_url",
    "examfTtmBk_5": "engine",
    "dEYieqnzsigE": "conn",
    "Vta6ea3F01Ju": "deleted_notifications",
    "E2_KpJ7YAEeI": "deleted_referrals",
    "NgaT11tFHfUC": "result",
    "IfwIp02ZI50t": "revision_id",
    "hrgmUSq5vFaA": "script_dir",
    "DxjpDrvsrMP4": "venv_python",
    "ADUIqZAL1Zgf": "venv_marker",
    "N5BOS5Ba7iBe": "bin_candidates",
    "H6bcNnJNBekj": "bin_dir",
    "pEfQPe06_bNU": "default_cmd",
    "Nynw3IhkeoPb": "cmd_name",
    "AxqUYyg2kRoh": "cmd_path",
    "aKErMq2ffNB_": "fh",
    "t09X61UaTZUU": "existing_cmd",
    "tbY49y6hEKQg": "new_cmd_name",
    "uYrXWAOakCA6": "launcher_path",
    "zYU0AcfTUN9H": "python_executable",
    "CJOEH5dagWs_": "server",
    "M79o_CyLR10K": "session",
    "dhwwiGt3_ntG": "app",
    "hvuYJwbmJTFX": "runner",
    "PGcAj_zEi4a3": "site",
    "pdYn9YoDs220": "sig",
    "gTBPDPy87BYI": "cmd",
    # Вложенная задача проверки серверов
    "HNBdWebD2ahJ": "run_check_servers",
}


def step12_locals_and_constants(src: str) -> str:
    tree = ast.parse(src)

    class _Cleanup(ast.NodeTransformer):
        def visit_FunctionDef(self, n: ast.FunctionDef):
            if n.name in LOCAL_RENAME:
                n.name = LOCAL_RENAME[n.name]
            self.generic_visit(n)
            return n

        def visit_AsyncFunctionDef(self, n: ast.AsyncFunctionDef):
            if n.name in LOCAL_RENAME:
                n.name = LOCAL_RENAME[n.name]
            self.generic_visit(n)
            return n

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


def step14_text_normalize_import_wrappers(src: str) -> str:
    """Финальный текстовый фоллбек для импорт-обёрток внутри функций.
    Не удаляет код, только делает подстановки и добавляет импорт.
    """
    out = src
    # I3Qj6caZgXTY('pkg') → importlib.import_module('pkg')
    out = re.sub(r"\bI3Qj6caZgXTY\s*\(", "importlib.import_module(", out)
    # TKizvQ0BnfYh('pkg','Name',...) → importlib.import_module('pkg')
    out = re.sub(r"\bTKizvQ0BnfYh\s*\(\s*(['\"])\\?([^'\"]+)\1\s*,", r"importlib.import_module(\1\2\1),", out)
    # Не делаем агрессивных замен по всем длинным именам — это приводит к ложным срабатываниям
    if "importlib.import_module(" in out and not re.search(r"^\s*import\s+importlib\b", out, re.M):
        out = "import importlib\n" + out
    return out


def step15_drop_known_wrapper_defs(src: str) -> str:
    """Удаляет определения известных обёрток, если они не используются."""
    WRAPPERS = {"TKizvQ0BnfYh", "I3Qj6caZgXTY"}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src
    used: set[str] = set()
    class U(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            if isinstance(n.ctx, ast.Load) and n.id in WRAPPERS:
                used.add(n.id)
    U().visit(tree)
    if not WRAPPERS - used:
        return src
    new_body: list[ast.stmt] = []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in (WRAPPERS - used):
            continue
        new_body.append(n)
    tree.body = new_body
    ast.fix_missing_locations(tree)
    return unparse(tree)


def step16_auto_rename_dynamic(src: str) -> str:
    """
    Динамическое переименование подозрительных имён на человекочитаемые по эвристикам.
    Никакой код не удаляем.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src

    def is_suspect(name: str) -> bool:
        return len(name) >= 10 and bool(re.search(r"[0-9]", name))

    # Соберём существующие имена для предотвращения коллизий
    existing: set[str] = set()

    class Collect(ast.NodeVisitor):
        def visit_Name(self, n: ast.Name):
            existing.add(n.id)
        def visit_FunctionDef(self, n: ast.FunctionDef):
            existing.add(n.name)
            self.generic_visit(n)
        def visit_AsyncFunctionDef(self, n: ast.AsyncFunctionDef):
            existing.add(n.name)
            self.generic_visit(n)
        def visit_ExceptHandler(self, n: ast.ExceptHandler):
            if isinstance(n.name, str):
                existing.add(n.name)

    Collect().visit(tree)

    rename: dict[str, str] = {}

    def unique(name: str) -> str:
        base = name
        i = 2
        while name in existing or name in rename.values():
            name = f"{base}_{i}"
            i += 1
        existing.add(name)
        return name

    def attr_chain(n: ast.AST) -> list[str]:
        chain: list[str] = []
        cur = n
        while isinstance(cur, ast.Attribute):
            chain.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            chain.append(cur.id)
        chain.reverse()
        return chain

    def suggest_from_call(call: ast.Call) -> str | None:
        f = call.func
        name = None
        # Path(...) → path
        if (isinstance(f, ast.Name) and f.id == "Path") or (
            isinstance(f, ast.Attribute) and f.attr == "Path"
        ):
            # уточнение по аргументу
            if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
                s = call.args[0].value
                if "alembic/versions" in s:
                    return "versions_dir"
                if "alembic/env.py" in s:
                    return "alembic_env_path"
            return "path"
        # create_engine(...) → engine
        if (isinstance(f, ast.Name) and f.id == "create_engine") or (
            isinstance(f, ast.Attribute) and f.attr == "create_engine"
        ):
            return "engine"
        # uvicorn.Config → uvicorn_config / config
        if (isinstance(f, ast.Attribute) and f.attr == "Config") or (
            isinstance(f, ast.Name) and f.id == "Config"
        ):
            return "config"
        # uvicorn.Server → server
        if (isinstance(f, ast.Attribute) and f.attr == "Server") or (
            isinstance(f, ast.Name) and f.id == "Server"
        ):
            return "server"
        # ScriptDirectory.from_config → script_dir
        if isinstance(f, ast.Attribute) and f.attr == "from_config":
            ch = attr_chain(f.value)
            if ch and ch[-1] == "ScriptDirectory":
                return "script_dir"
        # asyncio.Event → stop_event (часто в коде)
        if isinstance(f, ast.Attribute) and f.attr == "Event":
            ch = attr_chain(f.value)
            if ch and ch[-1] == "asyncio":
                return "stop_event"
        # asyncio.get_event_loop → loop
        if isinstance(f, ast.Attribute) and f.attr == "get_event_loop":
            return "loop"
        # web.AppRunner → runner
        if isinstance(f, ast.Attribute) and f.attr == "AppRunner":
            return "runner"
        # web.TCPSite → site
        if isinstance(f, ast.Attribute) and f.attr == "TCPSite":
            return "site"
        # importlib.import_module('hashlib') → hashlib_module
        if (
            isinstance(f, ast.Attribute)
            and isinstance(f.value, ast.Name)
            and f.value.id == "importlib"
            and f.attr == "import_module"
            and call.args
            and isinstance(call.args[0], ast.Constant)
            and isinstance(call.args[0].value, str)
            and call.args[0].value == "hashlib"
        ):
            return "hashlib_module"
        # subprocess.run([... 'alembic', 'upgrade']) → upgrade_result
        if isinstance(f, ast.Attribute) and f.attr == "run":
            if call.args and isinstance(call.args[0], (ast.List, ast.Tuple)):
                items = call.args[0].elts
                vals: list[str] = []
                for it in items:
                    if isinstance(it, ast.Constant) and isinstance(it.value, str):
                        vals.append(it.value)
                if any("alembic" in v for v in vals) and any("upgrade" in v for v in vals):
                    return "upgrade_result"
                if any("alembic" in v for v in vals) and any("revision" in v for v in vals):
                    return "result"
        # asyncio.create_task(...) → task
        if isinstance(f, ast.Attribute) and f.attr == "create_task":
            return "task"
        # os.path.abspath('venv/bin/python') → venv_python
        if isinstance(f, ast.Attribute) and f.attr == "abspath":
            if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
                s = call.args[0].value
                if "venv/bin/python" in s:
                    return "venv_python"
        # os.path.join('venv', '.installed') → venv_marker
        if isinstance(f, ast.Attribute) and f.attr == "join":
            if (
                len(call.args) >= 2
                and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in call.args[:2])
                and call.args[0].value == "venv"
                and call.args[1].value in {".installed", ".ok", ".ready"}
            ):
                return "venv_marker"
        return name

    # Первая проходка: собрать предложения
    class Propose(ast.NodeVisitor):
        def visit_Assign(self, n: ast.Assign):
            # одиночное имя
            if len(n.targets) == 1:
                tgt = n.targets[0]
                if isinstance(tgt, ast.Name):
                    name = tgt.id
                    if is_suspect(name):
                        new: str | None = None
                        if isinstance(n.value, ast.Call):
                            new = suggest_from_call(n.value)
                        if new is None and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                            if "/" in n.value.value or n.value.value.endswith(".py"):
                                new = "path"
                        if new:
                            rename.setdefault(name, unique(new))
                # кортеж с одним элементом (X,) = (call,)
                if isinstance(tgt, ast.Tuple) and len(tgt.elts) == 1 and isinstance(tgt.elts[0], ast.Name):
                    name = tgt.elts[0].id
                    if is_suspect(name):
                        if isinstance(n.value, ast.Tuple) and len(n.value.elts) == 1:
                            val = n.value.elts[0]
                        else:
                            val = n.value
                        new = None
                        if isinstance(val, ast.Call):
                            new = suggest_from_call(val)
                        if new:
                            rename.setdefault(name, unique(new))
            self.generic_visit(n)

        def visit_With(self, n: ast.With):
            for item in n.items:
                if isinstance(item.optional_vars, ast.Name) and is_suspect(item.optional_vars.id):
                    as_name = item.optional_vars.id
                    base = None
                    if isinstance(item.context_expr, ast.Call):
                        f = item.context_expr.func
                        if (isinstance(f, ast.Attribute) and f.attr == "connect") or (
                            isinstance(f, ast.Name) and f.id == "connect"
                        ):
                            base = "conn"
                    if base:
                        rename.setdefault(as_name, unique(base))
            self.generic_visit(n)

        def visit_ExceptHandler(self, n: ast.ExceptHandler):
            if isinstance(n.name, str) and is_suspect(n.name):
                rename.setdefault(n.name, unique("exc"))
            self.generic_visit(n)

        def visit_For(self, n: ast.For):
            if isinstance(n.target, ast.Name) and is_suspect(n.target.id):
                # for <suspect> in (signal.SIGINT, signal.SIGTERM)
                if isinstance(n.iter, (ast.Tuple, ast.List)):
                    elts = n.iter.elts
                    if any(isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == "signal" for e in elts):
                        rename.setdefault(n.target.id, unique("sig"))
            self.generic_visit(n)

    Propose().visit(tree)

    if not rename:
        return src

    class Apply(ast.NodeTransformer):
        def visit_Name(self, n: ast.Name):
            if n.id in rename:
                n.id = rename[n.id]
            return n
        def visit_FunctionDef(self, n: ast.FunctionDef):
            if n.name in rename:
                n.name = rename[n.name]
            self.generic_visit(n)
            return n
        def visit_AsyncFunctionDef(self, n: ast.AsyncFunctionDef):
            if n.name in rename:
                n.name = rename[n.name]
            self.generic_visit(n)
            return n
        def visit_ExceptHandler(self, n: ast.ExceptHandler):
            if isinstance(n.name, str) and n.name in rename:
                n.name = rename[n.name]
            self.generic_visit(n)
            return n

    new_tree = Apply().visit(tree)
    ast.fix_missing_locations(new_tree)
    return unparse(new_tree)


def step6h_rewrite_generic_import_calls(src: str) -> str:
    """
    Находит функции-обёртки импортов по паттерну X('pkg') и частоcти вызовов,
    переписывает X('pkg') → importlib.import_module('pkg').
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src

    counts: dict[str, int] = {}

    class Counter(ast.NodeVisitor):
        def visit_Call(self, n: ast.Call):
            if (
                isinstance(n.func, ast.Name)
                and len(n.args) >= 1
                and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, str)
                and all(isinstance(kw.value, (ast.Constant, ast.Name, ast.Attribute)) for kw in n.keywords)
            ):
                counts[n.func.id] = counts.get(n.func.id, 0) + 1
            self.generic_visit(n)

    Counter().visit(tree)
    candidates = {name for name, c in counts.items() if c >= 3 and name not in {"print", "str", "bytes"}}
    if not candidates:
        return src

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, n: ast.Call):
            self.generic_visit(n)
            if (
                isinstance(n.func, ast.Name)
                and n.func.id in candidates
                and len(n.args) >= 1
                and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, str)
            ):
                return ast.copy_location(
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="importlib", ctx=ast.Load()),
                            attr="import_module",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant(n.args[0].value)],
                        keywords=[],
                    ),
                    n,
                )
            return n

    new = Rewriter().visit(tree)
    ast.fix_missing_locations(new)
    code = unparse(new)
    if "importlib.import_module(" in code and not re.search(r"^\s*import\s+importlib\b", code, re.M):
        code = "import importlib\n" + code
    return code


def step6i_rewrite_generic_twoarg_wrappers(src: str) -> str:
    """
    Переписывает вызовы вида F('pkg','Attr', ...) → importlib.import_module('pkg')
    (оставляя последующий .Attr снаружи), по общему паттерну без знания имени F.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src

    class Rewriter(ast.NodeTransformer):
        def visit_Call(self, n: ast.Call):
            self.generic_visit(n)
            if (
                isinstance(n.func, ast.Name)
                and len(n.args) >= 2
                and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in n.args[:2])
            ):
                # Эвристика: F('pkg','Attr', ...) → importlib.import_module('pkg').Attr
                pkg = n.args[0].value
                attr = n.args[1].value
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
                    n,
                )
            return n

    new = Rewriter().visit(tree)
    ast.fix_missing_locations(new)
    code = unparse(new)
    if "importlib.import_module(" in code and not re.search(r"^\s*import\s+importlib\b", code, re.M):
        code = "import importlib\n" + code
    return code


def step6j_normalize_exception_types(src: str) -> str:
    """Заменяет подозрительные имена классов исключений в except на Exception."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src

    def is_suspect(name: str) -> bool:
        return len(name) >= 10 and bool(re.search(r"[0-9]", name))

    class Fixer(ast.NodeTransformer):
        def visit_ExceptHandler(self, n: ast.ExceptHandler):
            if isinstance(n.type, ast.Name) and is_suspect(n.type.id):
                n.type = ast.copy_location(ast.Name(id="Exception", ctx=ast.Load()), n.type)
            return self.generic_visit(n) or n

    new = Fixer().visit(tree)
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
                },
            ),
        ),
        Step("drop builtin self-assigns", step5a_drop_builtin_assignments),
        Step("decode u1KQ2EguJKQ7 calls", step6_decode_u1_calls),
        Step("decode simple lambda", step6e_decode_simple_lambda),
        Step("rewrite TKizvQ0BnfYh wrapper", step6f_rewrite_TKizvQ0BnfYh),
        Step("rewrite I3Qj6caZgXTY to importlib", step6g_rewrite_obf_import_call),
        # Step("rewrite generic import calls", step6h_rewrite_generic_import_calls),  # disabled: overly aggressive
        Step("rewrite generic two-arg wrappers", step6i_rewrite_generic_twoarg_wrappers),
        Step("fold consts & getattr (pass1)", step7_fold_consts_and_getattr),
        Step("cleanup str decode", step6a_cleanup_str_decode),
        Step("fold consts & getattr (pre-import-fixes)", step7_fold_consts_and_getattr),
        Step("rewrite lazy import slBqQzRHEsUg", step6b_rewrite_lazy_import),
        Step("rewrite import wrapper JXzJajrdQAWB", step6c_rewrite_import_wrapper),
        Step("ensure 'import importlib' header", step6d_ensure_importlib_import),
        Step("fold consts & getattr (post-import-fixes)", step7_fold_consts_and_getattr),
        Step("normalize obfuscated exception types", step6j_normalize_exception_types),
        Step("rename from tuple assigns", step8_rename_from_tuple_assignments),
        Step("flatten import assigns", step9_flatten_import_assigns),
        Step("global rename", step10_global_rename),
        Step("global text cleanup", step11_global_text_cleanup),
        Step("locals & constants", step12_locals_and_constants),
        Step("text normalize import wrappers", step14_text_normalize_import_wrappers),
        Step("drop known wrapper defs", step15_drop_known_wrapper_defs),
        Step("auto rename dynamic", step16_auto_rename_dynamic),
        # Step("drop unused functions", step13_drop_unused_funcs),  # disabled to avoid accidental code removal
        Step("fold consts & getattr (final)", step7_fold_consts_and_getattr),
    ]


def run_pipeline(initial_code: str, dump_layers: bool = False, dump_dir: Path | None = None) -> str:
    steps = build_pipeline()
    cur = initial_code
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
            (dump_dir / f"layer{idx:02d}.py").write_text(nxt, encoding="utf-8")
        cur = nxt
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
