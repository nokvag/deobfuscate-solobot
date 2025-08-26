# -*- coding: utf-8 -*-
"""
auto_peel.py
~~~~~~~~~~~~
Полный автоматический «сниматель» многослойной Python‑обфускации.

Запускайте из каталога с `layer4.py` (или другим стартовым слоем) ­—
скрипт будет:

1. Подменять `exec`/`eval` и собирать любой выполняемый текст.
2. Автоматически создавать «заглушки» для недостающих пакетов
   (универсальный `_StubModule`).
3. Поддерживать `_tuple_new` (нужен обфускатору вместо `namedtuple`).
4. Сохранять каждый пойманный слой в `layer<N>_raw.py`.
5. Останавливаться, когда новый код больше не генерируется.

Использовать **только внутри изолированной среды**!
"""
from __future__ import annotations

import builtins
import pathlib
import runpy
import sys
import types
from typing import List, Tuple

# ──────────────────────────────────────────────────────────────
# 0.  Заглушки для исключений Python 3.11+ (если скрипт идёт на 3.10)
if sys.version_info < (3, 11):
    class _Dummy(Exception):
        ...
    for _name in ("BaseExceptionGroup", "ExceptionGroup"):
        if not hasattr(builtins, _name):
            setattr(builtins, _name, type(_name, (_Dummy,), {}))

# ──────────────────────────────────────────────────────────────
# 1.  Универсальный модуль‑заглушка
class _StubModule(types.ModuleType):
    """Пустой, но «толерантный» модуль‑заглушка."""
    def __init__(self, name: str):
        super().__init__(name)
        self.__dict__["__path__"] = []  # пусть считается пакетом

    def __getattr__(self, item: str):
        if item == "__path__":
            return self.__dict__["__path__"]
        sub = _StubModule(f"{self.__name__}.{item}")
        setattr(self, item, sub)
        return sub

    def __call__(self, *a, **kw):
        return self                      # поддержка цепочек вызовов

    def __iter__(self):
        return iter(())

# Предзагружаем самые частые внешние модули
_PRELOAD_STUBS = (
    "aiogram", "aiogram.types", "aiogram.filters", "aiogram.utils",
    "aiogram.methods", "aiogram.fsm", "aiohttp", "msvcrt",
)
for _mod in _PRELOAD_STUBS:
    sys.modules.setdefault(_mod, _StubModule(_mod))

# ──────────────────────────────────────────────────────────────
# 2.  Подмена __import__: создаём StubModule «на лету»
_orig_import = builtins.__import__
def _stub_import(name, globals=None, locals=None, fromlist=(), level=0):
    try:
        return _orig_import(name, globals, locals, fromlist, level)
    except ModuleNotFoundError as exc:
        missing = exc.name or name
        parts = missing.split(".")
        for i in range(1, len(parts) + 1):
            sub = ".".join(parts[:i])
            sys.modules.setdefault(sub, _StubModule(sub))
        return _orig_import(name, globals, locals, fromlist, level)
builtins.__import__ = _stub_import

# ──────────────────────────────────────────────────────────────
# 3.  Мини‑реализация _tuple_new (замена namedtuple.__new__)
def _tuple_new(cls, values: Tuple):
    return tuple.__new__(cls, values)
builtins._tuple_new = _tuple_new

# ──────────────────────────────────────────────────────────────
# 4.  Перехватчики exec / eval
class _ExecInterceptor:
    def __init__(self):
        self.captured: List[str] = []
        self._orig_exec = builtins.exec
        self._orig_eval = builtins.eval

    def _exec(self, src, g=None, l=None):
        self._save(src)
        return self._orig_exec(src, g, l)

    def _eval(self, src, g=None, l=None):
        if isinstance(src, str):
            self.captured.append(src)
        return self._orig_eval(src, g, l)

    def _save(self, src):
        if isinstance(src, (str, bytes, bytearray)):
            try:
                self.captured.append(
                    src.decode() if isinstance(src, (bytes, bytearray)) else src
                )
            except Exception:
                pass

    def install(self):
        builtins.exec, builtins.eval = self._exec, self._eval

    def restore(self):
        builtins.exec, builtins.eval = self._orig_exec, self._orig_eval

# ──────────────────────────────────────────────────────────────
# 5.  Снимаем один слой
def peel_layer(input_path: pathlib.Path, level: int) -> Tuple[int, pathlib.Path]:
    interceptor = _ExecInterceptor()
    interceptor.install()
    try:
        if input_path.suffix == ".py":
            runpy.run_path(str(input_path), run_name="__main__")
        else:
            exec(input_path.read_text(encoding="utf-8"), {})
    finally:
        interceptor.restore()

    next_path = input_path.parent / f"layer{level+1}_raw.py"
    if interceptor.captured:
        next_path.write_text(
            "\n\n# -------------- NEXT CHUNK --------------\n\n".join(interceptor.captured),
            encoding="utf-8"
        )
    return len(interceptor.captured), next_path

# ──────────────────────────────────────────────────────────────
# 6.  Главный цикл
def main(start_file: str = "layer4.py", max_layers: int = 50):
    current = pathlib.Path(start_file).resolve()
    if not current.exists():
        sys.exit(f"❌ Стартовый файл {current} не найден.")

    level = int("".join(filter(str.isdigit, current.stem)) or "4")
    print(f"[▶] Старт: {current} (слой {level})")

    while level - int("".join(filter(str.isdigit, current.stem)) or level) < max_layers:
        count, nxt = peel_layer(current, level)
        if count == 0:
            print(f"✅ Слой {level} оказался финальным — новый код не генерируется.")
            break
        print(f"[+] Слой {level} → {level+1}: поймано {count} фрагм., сохранено в {nxt.name}")
        current, level = nxt, level + 1
    else:
        print("⚠️  Достигнут предел max_layers; возможно, ещё остаются слои.")

if __name__ == "__main__":
    main()