import re
from typing import ByteString

KEY = bytes.fromhex(
    '3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00031e18071d0f1a0a'
)

def xor_transform(data: ByteString, key: bytes = KEY) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def extract_xor_blocks(code: str) -> list[tuple[str, str]]:
    # Найти все b'...' строки, переданные в xor_transform()
    pattern = r'xor_transform\(\s*b([\'"])(.*?)\1\s*\)'
    return [(match[1], match[0]) for match in re.findall(pattern, code)]

def replace_xor_calls_with_plaintext(code: str) -> str:
    pattern = r'xor_transform\(\s*b([\'"])(.*?)\1\s*\)'

    def replacer(match):
        quote = match.group(1)
        hex_bytes = match.group(2).encode('latin1')  # byte string, not escaped
        try:
            raw_bytes = eval(f"b{quote}{match.group(2)}{quote}")  # safely parse b'...'
            decoded = xor_transform(raw_bytes).decode('utf-8', errors='replace')
            # Возвращаем как строку с комментарием (или f"'{decoded}'" для замены)
            return f'"{decoded}"  # ← decoded from xor_transform(...)'
        except Exception as e:
            return f'xor_transform(b{quote}{match.group(2)}{quote})  # ⚠️ decode error: {e}'

    return re.sub(pattern, replacer, code)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Использование: python xor_decoder.py <обфусцированный_файл.py>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        code = f.read()

    transformed = replace_xor_calls_with_plaintext(code)

    output_file = sys.argv[1].replace('.py', '_decoded.py')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transformed)

    print(f"✅ Декод завершён. Сохранено в: {output_file}")
