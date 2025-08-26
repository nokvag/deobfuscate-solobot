#!/usr/bin/env python3
import re, ast, sys,base64,gzip

# Регулярка для поиска hex‑литерала внутри exec‑вызова или _('…'):
PAT = re.compile(
    r"""
    (?:exec|_)        # либо exec, либо вызов функции-алиаса _
    \s*               # пробелы
    \(\s*             # открывающая скобка
      (['"])(.*?)\1   # строковый литерал в '…' или "…"
    \s*\)
    """,
    re.S | re.X,
)

def unwrap_once(src: str) -> str:
    m = PAT.search(src)
    if not m:
        return None
    lit = m.group(2)
    # Превращаем в реальный Python-литерал (учтёт экранированные \\ и т.п.)
    py_lit = f"'{lit}'"
    unesc = ast.literal_eval(py_lit)
    # \xNN → байт → символ
    return unesc.encode('latin1').decode('unicode_escape', errors='replace')

def deobfuscate(src: str) -> str:
    layer = 0
    while True:
        nxt = unwrap_once(src)
        if nxt is None:
            break
        src = nxt
        layer += 1
        # Вы можете раскомментировать строку ниже, чтобы видеть прогресс:
        # print(f"--- слой {layer} распакован ({len(src)} байт) ---", file=sys.stderr)
    return src

def extract_numbers(pattern, text, description):
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"Не найден {description}.", file=sys.stderr)
        sys.exit(1)
    nums_str = m.group(1)
    return [int(x) for x in re.findall(r'\d+', nums_str)]

def deobfuscate_layer3(decoded_l2):


    # 1) ключ: _ = [ ... ]
    key = extract_numbers(r"_\s*=\s*\[([^\]]+)\]", decoded_l2, "первый список (ключ)")

    # 2) данные: enumerate( [ ... ] )
    data = extract_numbers(r"enumerate\s*\(\s*\[([^\]]+)\]\s*\)", decoded_l2, "второй список (данные)")

    # декодим
    decoded_bytes = bytearray()
    key_len = len(key)
    for idx, b in enumerate(data):
        decoded_bytes.append(b ^ key[idx % key_len])

    try:
        decoded = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        decoded = decoded_bytes.decode('utf-8', errors='replace')
    return decoded


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: deobf_smart.py <obf.py>", file=sys.stderr)
        sys.exit(1)

    inp = sys.argv[1]
    txt = open(inp, 'r', encoding='utf-8', errors='ignore').read()
        #layer 1
    result = deobfuscate(txt)
    #layer 2
    m = re.search(r"b'([^']+)'", result, re.DOTALL)
    if not m:
        raise RuntimeError("Не найден b85-блок")
    data = m.group(1).encode('utf-8')
    decoded_l2 = base64.b85decode(data)
    decoded_l3=deobfuscate_layer3(decoded_l2)
    # layer 3   
    #print(decoded_l3)
    #print(decoded.decode('utf-8', 'ignore'))
    sys.stdout.write(decoded_l3)