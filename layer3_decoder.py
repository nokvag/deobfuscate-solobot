#!/usr/bin/env python3
import re
import sys

def extract_numbers(pattern, text, description):
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"Не найден {description}.", file=sys.stderr)
        sys.exit(1)
    nums_str = m.group(1)
    return [int(x) for x in re.findall(r'\d+', nums_str)]

def deobfuscate(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        src = f.read()

    # 1) ключ: _ = [ ... ]
    key = extract_numbers(r"_\s*=\s*\[([^\]]+)\]", src, "первый список (ключ)")

    # 2) данные: enumerate( [ ... ] )
    data = extract_numbers(r"enumerate\s*\(\s*\[([^\]]+)\]\s*\)", src, "второй список (данные)")

    # декодим
    decoded_bytes = bytearray()
    key_len = len(key)
    for idx, b in enumerate(data):
        decoded_bytes.append(b ^ key[idx % key_len])

    try:
        decoded = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        decoded = decoded_bytes.decode('utf-8', errors='replace')

    # сохраняем
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decoded)

    print(f"Успешно декодировано и записано в {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Использование: {sys.argv[0]} layer2.py deobfuscated.py", file=sys.stderr)
        sys.exit(1)
    deobfuscate(sys.argv[1], sys.argv[2])