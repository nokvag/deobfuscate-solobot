import builtins, io, re, tokenize
from types import MappingProxyType

def deobfuscate_builtins(source: str,
                         keep: set[str] | None = None) -> str:
    """
    Заменяет фальш-идентификаторы на настоящие имена объектов builtins.
    Параметр *keep* позволяет деобфусцировать выборочно, оставив
    остальные псевдонимы нетронутыми.
    """
    # 1. Находим строчку вида  «foo,bar = Foo,Bar»
    m = re.search(r"^(.*?)=(.*)$", source, flags=re.S | re.M)
    if not m:
        return source                      # карты присваивания нет

    fake_names   = [s.strip() for s in m.group(1).split(",")]
    real_names   = [s.strip() for s in m.group(2).split(",")]
    built_names  = set(dir(builtins))

    mapping: dict[str, str] = {
        fake: real
        for fake, real in zip(fake_names, real_names)
        if real in built_names and (keep is None or real in keep)
    }
    if not mapping:
        return source

    mapping = MappingProxyType(mapping)    # read-only защитa

    # 2. Токенизируем и подменяем только идентификаторы кода
    out = []
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    for tok_type, tok_val, *rest in tokens:
        if tok_type == tokenize.NAME and tok_val in mapping:
            tok_val = mapping[tok_val]
        out.append((tok_type, tok_val, *rest))

    result = tokenize.untokenize(out)
    # в старых версиях (<3.7) вернётся bytes, в новых — str
    if isinstance(result, bytes):
        result = result.decode()
    return result

# --- пример использования ----------------------------------------
if __name__ == "__main__":
    with open("layer4.py", "r", encoding="utf-8") as f:
        code = f.read()

    # снимаем маски только с наиболее полезных builtins
    cleaned = deobfuscate_builtins(code, keep={"getattr", "print", "len",
                                               "open", "range"})

    with open("stage1_unmasked.py", "w", encoding="utf-8") as f:
        f.write(cleaned)