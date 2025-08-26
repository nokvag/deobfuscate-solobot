#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import ast
from typing import ByteString, Union

# Ключ для xor_transform из исходного файла
KEY = bytes.fromhex(
    '3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00031e18071d0f1a0a'
)

def xor_transform(data: ByteString, key: bytes=KEY) -> bytes:
    """
    Универсальная функция XOR‑преобразования из layer10.py.
    Для исходного алгоритма ENCRYPT == DECRYPT.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('data must be bytes‑like object')
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def decode_string(obj, *a, **kw):
    """Исходная функция decode из layer10.py"""
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj

def extract_xor_transform_calls(code: str) -> list:
    """Извлекает все вызовы xor_transform из кода"""
    pattern = r'xor_transform\(\s*b([\'"])(.*?)(\1)\s*\)'
    matches = re.finditer(pattern, code)
    result = []
    
    for match in matches:
        try:
            quote = match.group(1)
            raw_bytes_str = match.group(2)
            raw_bytes = eval(f"b{quote}{raw_bytes_str}{quote}")
            decrypted = xor_transform(raw_bytes)
            result.append((match.group(0), decrypted))
        except Exception as e:
            print(f"Ошибка при декодировании {match.group(0)}: {e}")
    
    return result

def replace_xor_calls(code: str) -> str:
    """Заменяет все вызовы xor_transform их декодированными значениями"""
    xor_calls = extract_xor_transform_calls(code)
    
    for call, decrypted in xor_calls:
        try:
            # Пробуем декодировать как UTF-8
            decoded = decrypted.decode('utf-8', errors='replace')
            # Заменяем вызов на строковый литерал
            code = code.replace(call, f'"{decoded}"')
        except Exception as e:
            print(f"Не удалось декодировать {call}: {e}")
    
    return code

def cleanup_chr_expressions(code: str) -> str:
    """Упрощает выражения с chr()"""
    # Паттерн для поиска chr(выражение)
    pattern = r'chr\((.*?)\)'
    
    def replacer(match):
        expr = match.group(1)
        try:
            # Вычисляем выражение внутри chr()
            value = eval(expr)
            char = chr(value)
            # Возвращаем символ в виде строкового литерала
            return f'"{char}"'
        except:
            return match.group(0)
    
    return re.sub(pattern, replacer, code)

def resolve_string_operations(code: str) -> str:
    """Упрощает операции конкатенации строк и вызовы decode"""
    # Заменяем очевидные вызовы decode
    decode_pattern = r'decode\(([^)]+)\)'
    
    def decode_replacer(match):
        arg = match.group(1)
        if "utf-8" in arg or "'u' + 't' + 'f'" in arg:
            return '"utf-8"'
        try:
            # Если аргумент - выражение, которое можно вычислить
            value = eval(arg)
            if isinstance(value, str):
                return f'"{value}"'
        except:
            pass
        return match.group(0)
    
    # Заменяем вызовы decode
    code = re.sub(decode_pattern, decode_replacer, code)
    
    # Упрощаем конкатенацию строк
    concat_pattern = r'"([^"]*)"\s*\+\s*"([^"]*)"'
    while re.search(concat_pattern, code):
        code = re.sub(concat_pattern, lambda m: f'"{m.group(1)}{m.group(2)}"', code)
    
    return code

def simplify_getattr_calls(code: str) -> str:
    """Упрощает вызовы getattr(obj, 'method')() в obj.method()"""
    # Паттерн для поиска getattr(obj, 'method')
    pattern = r'getattr\(([^,]+),\s*[\'"]([^\'"]+)[\'"]\)'
    
    def getattr_replacer(match):
        obj = match.group(1).strip()
        method = match.group(2)
        return f"{obj}.{method}"
    
    return re.sub(pattern, getattr_replacer, code)

def remove_dummy_code(code: str) -> str:
    """Удаляет код-заглушки и неиспользуемые переменные"""
    # Удаляем асинхронную функцию-заглушку
    code = re.sub(r'async def _dummy\(\*a, \*\*kw\):\s+pass\n', '', code)
    
    # Удаляем строки с присваиванием переменных, которые нигде не используются
    # Это может быть опасно, поэтому лучше делать вручную, здесь просто пример
    return code

def deobfuscate(input_file, output_file):
    """Основная функция деобфускации"""
    print(f"Начинаю деобфускацию файла {input_file}")
    
    # Чтение содержимого файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Сохраняем копию исходного кода для сравнения
    original_code = code
    
    # Итеративная деобфускация
    iterations = 3
    for i in range(iterations):
        print(f"Итерация {i+1}/{iterations}:")
        
        # Шаг 1: Заменяем вызовы xor_transform
        print("  Декодирование вызовов xor_transform...")
        code = replace_xor_calls(code)
        
        # Шаг 2: Упрощаем выражения с chr()
        print("  Упрощение выражений с chr()...")
        code = cleanup_chr_expressions(code)
        
        # Шаг 3: Упрощаем строковые операции
        print("  Упрощение строковых операций...")
        code = resolve_string_operations(code)
        
        # Шаг 4: Упрощаем вызовы getattr
        print("  Упрощение вызовов getattr...")
        code = simplify_getattr_calls(code)
        
        # Сохраняем промежуточный результат
        intermediate_file = f"{output_file.rsplit('.', 1)[0]}_iteration{i+1}.py"
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"  Сохранен промежуточный результат: {intermediate_file}")
        
        # Проверяем, есть ли изменения
        if code == original_code:
            print(f"  Нет изменений после итерации {i+1}, завершаем")
            break
        
        original_code = code
    
    # Сохраняем итоговый результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"Деобфускация завершена, результат сохранен в {output_file}")
    print("""
Для дальнейшей деобфускации рекомендуется:
1. Проанализировать полученный код и выявить общие паттерны обфускации
2. Вручную заменить обфусцированные имена переменных и функций на осмысленные
3. Упростить сложные конструкции кода
4. Использовать инструменты для форматирования кода (black, autopep8)
""")

def final_manual_cleanup(code: str) -> str:
    """
    Функция для ручной очистки и форматирования кода.
    Эта функция должна применяться после автоматической деобфускации
    для устранения специфических паттернов и улучшения читаемости.
    """
    # Примеры ручной очистки:
    
    # 1. Удаление или замена определенных паттернов
    code = code.replace('__import__(\'utf-8\')', 'importlib.import_module(\'utf-8\')')
    
    # 2. Очистка кода, связанного с импортами
    code = re.sub(r'import importlib, builtins, types, sys\n+', 'import importlib\nimport builtins\nimport types\nimport sys\n\n', code)
    
    # 3. Замена обфусцированных переменных на более читаемые имена
    # Это требует ручного анализа и понимания кода
    var_mapping = {
        'diyel4O5bMLs': 'asyncio',
        'GiFJytvAvueM': 'bot',
        'zcptFAL0yWNU': 'logger',
        # и т.д.
    }
    
    for old_name, new_name in var_mapping.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python enhanced_decoder_layer10.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "layer10_enhanced_deobfuscated.py"
    
    deobfuscate(input_file, output_file) 