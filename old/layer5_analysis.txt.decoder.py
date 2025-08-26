#!/usr/bin/env python3
import re
import ast
import base64
import zlib
import marshal
import sys
import binascii
from types import CodeType

def decode_binary_string(s):
    """Декодирует строковое представление бинарных данных в байты."""
    result = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '\':
            if i + 1 < len(s) and s[i + 1] == 'x':
                if i + 3 < len(s):
                    try:
                        val = int(s[i+2:i+4], 16)
                        result.append(val)
                        i += 4
                        continue
                    except ValueError:
                        pass
            elif i + 1 < len(s):
                c = s[i + 1]
                if c == 'n':
                    result.append(10)  # \n
                elif c == 't':
                    result.append(9)   # \t
                elif c == 'r':
                    result.append(13)  # \r
                elif c == '0':
                    result.append(0)   # \0
                elif c == '\':
                    result.append(92)  # \\
                elif c == '"':
                    result.append(34)  # \"
                elif c == "'":
                    result.append(39)  # \'
                else:
                    result.append(ord(c))
                i += 2
                continue
        result.append(ord(s[i]))
        i += 1
    return bytes(result)

def decode_u1KQ2EguJKQ7(binary_str):
    """Декодирует данные из функции u1KQ2EguJKQ7."""
    try:
        # Шаг 1: Конвертируем строковое представление в байты
        binary_data = decode_binary_string(binary_str)
        
        # Шаг 2: Пробуем различные методы декодирования
        # Base64
        try:
            decoded = base64.b64decode(binary_data)
            return decoded.decode('utf-8', errors='replace')
        except:
            pass
        
        # Zlib
        try:
            decoded = zlib.decompress(binary_data)
            return decoded.decode('utf-8', errors='replace')
        except:
            pass
        
        # Если ничего не сработало, возвращаем исходную строку
        return binary_str
    except Exception as e:
        return f"[Ошибка декодирования: {e}]"

def extract_constants_from_tuple_assignment(code):
    """Извлекает переназначения встроенных функций и констант из начала файла."""
    pattern = r"\(\s*([\w,_\s]+)\s*\)\s*=\s*\(\s*([\w,_\s]+)\s*\)"
    match = re.search(pattern, code, re.DOTALL)
    
    if not match:
        return {}
    
    left_vars = [var.strip() for var in match.group(1).split(',')]
    right_vars = [var.strip() for var in match.group(2).split(',')]
    
    # Создаем словарь переназначений
    return {left: right for left, right in zip(left_vars, right_vars) if left and right}

def deobfuscate_file(input_file, output_file):
    """Декодирует файл layer5.py."""
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # 1. Восстанавливаем встроенные функции и константы
    constants_map = extract_constants_from_tuple_assignment(code)
    
    # 2. Заменяем обфусцированные имена на оригинальные
    deobfuscated_code = code
    for obf, real in constants_map.items():
        deobfuscated_code = re.sub(r'\b' + re.escape(obf) + r'\b', real, deobfuscated_code)
    
    # 3. Заменяем вызовы u1KQ2EguJKQ7
    pattern = r'u1KQ2EguJKQ7\s*\(\s*b"([^"]*)"\s*\)'
    matches = list(re.finditer(pattern, deobfuscated_code))
    
    # Обрабатываем с конца, чтобы не нарушать позиции при замене
    for match in reversed(matches):
        binary_str = match.group(1)
        decoded = decode_u1KQ2EguJKQ7(binary_str)
        deobfuscated_code = deobfuscated_code[:match.start()] + f'"{decoded}"' + deobfuscated_code[match.end():]
    
    # 4. Упрощаем вызовы t5NjExmI3vgw (это примерно, может потребоваться доработка)
    # pattern = r't5NjExmI3vgw\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)'
    # for match in reversed(list(re.finditer(pattern, deobfuscated_code))):
    #     func = match.group(1).strip()
    #     data = match.group(2).strip()
    #     deobfuscated_code = deobfuscated_code[:match.start()] + f"{func}({data})" + deobfuscated_code[match.end():]
    
    # 5. Записываем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Декодированный файл layer5.py\n\n")
        f.write(deobfuscated_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Использование: {sys.argv[0]} input_file output_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    deobfuscate_file(input_file, output_file)
    print(f"Файл декодирован и записан в {output_file}")
