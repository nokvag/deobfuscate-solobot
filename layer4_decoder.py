#!/usr/bin/env python3
import sys
import ast
import gzip

def deobfuscate_gzip_layer(input_path, output_path):
    # 1) прочитать исходник
    with open(input_path, 'r', encoding='utf-8') as f:
        src = f.read()

    # 2) распарсить AST
    try:
        tree = ast.parse(src, filename=input_path)
    except SyntaxError as e:
        print(f"Ошибка синтаксического разбора {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # 3) найти первый байтовый литерал
    blob = None
    for node in ast.walk(tree):
        # Python 3.8+: ast.Constant с .value типа bytes
        if isinstance(node, ast.Constant) and isinstance(node.value, (bytes, bytearray)):
            blob = node.value
            break
        # Для старых версий Python: ast.Bytes
        if hasattr(ast, 'Bytes') and isinstance(node, ast.Bytes):
            blob = node.s
            break

    if blob is None:
        print("Не найден байтовый литерал в AST.", file=sys.stderr)
        sys.exit(1)

    # 4) распаковать gzip
    try:
        decompressed = gzip.decompress(blob)
    except Exception as e:
        print("Ошибка при gzip.decompress:", e, file=sys.stderr)
        sys.exit(1)

    # 5) декодировать в текст
    try:
        text = decompressed.decode('utf-8')
    except UnicodeDecodeError:
        text = decompressed.decode('utf-8', errors='replace')

    # 6) сохранить результат
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Успешно распаковано и записано в {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Использование: {sys.argv[0]} <layer3.py> <decoded_layer4.py>", file=sys.stderr)
        sys.exit(1)
    deobfuscate_gzip_layer(sys.argv[1], sys.argv[2])