#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import ast
from typing import ByteString, Union
import os

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

def decode_bytes(obj, *a, **kw):
    """Исходная функция decode из layer10.py"""
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj

def extract_and_replace_xor_transform(code: str, debug=False) -> str:
    """Полностью заменяет все вызовы xor_transform их расшифрованными значениями"""
    # Находим все вызовы xor_transform с двоичными данными
    pattern = r'xor_transform\(\s*b([\'"])(.*?)(\1)\s*\)'
    
    def transform_match(match):
        try:
            quote = match.group(1)
            raw_bytes_str = match.group(2)
            # Преобразуем строку в байты 
            raw_bytes = eval(f"b{quote}{raw_bytes_str}{quote}")
            # Применяем xor_transform с ключом из layer10.py
            decrypted = xor_transform(raw_bytes)
            
            try:
                # Пробуем декодировать как UTF-8
                decoded = decrypted.decode('utf-8', errors='replace')
                # Возвращаем как строковый литерал и комментарий с оригиналом для отладки
                if debug:
                    return f'"{decoded}" /* {match.group(0)} */'
                else:
                    return f'"{decoded}"'
            except Exception as e:
                if debug:
                    return f'{match.group(0)} /* ошибка декодирования: {e} */'
                else:
                    return match.group(0)
                
        except Exception as e:
            if debug:
                return f'{match.group(0)} /* ошибка преобразования: {e} */'
            else:
                return match.group(0)
    
    return re.sub(pattern, transform_match, code)

def simplify_chr_expressions(code: str) -> str:
    """Упрощает все выражения с chr()"""
    pattern = r'chr\((.*?)\)'
    
    def evaluate_chr(match):
        expr = match.group(1)
        try:
            # Вычисляем выражение внутри chr()
            value = eval(expr)
            return f'"{chr(value)}"'
        except Exception:
            return match.group(0)
    
    return re.sub(pattern, evaluate_chr, code)

def simplify_int_expressions(code: str) -> str:
    """Упрощает выражения int('0o1', 8) и подобные"""
    pattern = r'int\([\'"]([^\'"]+)[\'"]\s*,\s*(\d+)\)'
    
    def evaluate_int(match):
        num_str = match.group(1)
        base = int(match.group(2))
        try:
            # Вычисляем выражение
            value = int(num_str, base)
            return str(value)
        except Exception:
            return match.group(0)
    
    return re.sub(pattern, evaluate_int, code)

def simplify_complex_expressions(code: str) -> str:
    """Упрощает сложные арифметические выражения и конкатенации строк"""
    # Упрощаем выражения вида (123 + 456)
    pattern_arithmetic = r'\((\d+\s*[\+\-\*\/]\s*\d+)\)'
    
    def evaluate_arithmetic(match):
        expr = match.group(1)
        try:
            value = eval(expr)
            return str(value)
        except Exception:
            return match.group(0)
    
    code = re.sub(pattern_arithmetic, evaluate_arithmetic, code)
    
    # Упрощаем конкатенации строк
    pattern_concat = r'(?<!")"([^"]*)"(?!")(?:\s*\+\s*"([^"]*)")+(?!")'
    
    def join_strings(match):
        parts = re.findall(r'"([^"]*)"', match.group(0))
        return f'{"".join(parts)}'
    
    # Находим и заменяем все конкатенации строк
    while re.search(pattern_concat, code):
        code = re.sub(pattern_concat, join_strings, code)
    
    return code

def simplify_decode_calls(code: str) -> str:
    """Упрощает вызовы функции decode()"""
    # Заменяем decode('u' + 't' + 'f' + '-' + '8') -> "utf-8"
    pattern = r'decode\(((?:[\'"][^\'\"]*[\'"](?:\s*\+\s*)?)+)\)'
    
    def decode_replacer(match):
        expr = match.group(1)
        try:
            # Если это простое строковое выражение
            value = eval(expr)
            return f'"{value}"'
        except Exception:
            return match.group(0)
    
    return re.sub(pattern, decode_replacer, code)

def clean_getattr_calls(code: str) -> str:
    """Заменяет getattr(obj, 'method') на obj.method"""
    # Базовый паттерн для getattr с простым строковым вторым аргументом
    pattern = r'getattr\(([^,]+),\s*[\'"]([^\'"]+)[\'"]\)'
    
    def getattr_replacer(match):
        obj = match.group(1).strip()
        method = match.group(2)
        return f"{obj}.{method}"
    
    return re.sub(pattern, getattr_replacer, code)

def fix_string_quotes(code: str) -> str:
    """Исправляет проблемы с кавычками в строках"""
    # Удаляем специальные последовательности вида "utf-8".decode('utf-8')
    pattern = r'"([^"]*)"\.(decode|encode)\([\'"][^\'"]*[\'"]\)'
    
    def fix_quotes(match):
        content = match.group(1)
        return f'"{content}"'
    
    return re.sub(pattern, fix_quotes, code)

def cleanup_imports(code: str) -> str:
    """Удаляет дублирующиеся импорты и упрощает их структуру"""
    # Паттерн для импортов
    lines = code.split('\n')
    cleaned_lines = []
    seen_imports = set()
    
    for line in lines:
        # Пропускаем повторяющиеся импорты
        if line.strip().startswith(('import ', 'from ')) and line.strip() in seen_imports:
            continue
            
        if line.strip().startswith(('import ', 'from ')):
            seen_imports.add(line.strip())
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def fix_broken_strings(code: str) -> str:
    """Исправляет явные ошибки в строках, где нет закрывающей кавычки или неправильная вложенность"""
    # Заменяем неправильные случаи типа "string.decode()
    pattern = r'"([^"]*)"\.(decode|utf-8)\(\)'
    
    def fix_string(match):
        content = match.group(1)
        return f'"{content}"'
    
    return re.sub(pattern, fix_string, code)

def deobfuscate_file(input_file, output_prefix, max_passes=5, debug=False):
    """Многопроходная деобфускация файла"""
    print(f"Начинаю деобфускацию файла {input_file}...")
    
    # Чтение исходного файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Сохраняем исходный код
    os.makedirs('deobfuscation_steps', exist_ok=True)
    with open(os.path.join('deobfuscation_steps', f"{output_prefix}_original.py"), 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Пошаговая деобфускация
    for i in range(max_passes):
        print(f"\nПроход {i+1}/{max_passes}:")
        previous_code = code
        
        # Шаг 1: Расшифровка вызовов xor_transform
        print("  Шаг 1: Расшифровка вызовов xor_transform...")
        code = extract_and_replace_xor_transform(code, debug)
        
        # Шаг 2: Упрощение выражений с chr()
        print("  Шаг 2: Упрощение выражений с chr()...")
        code = simplify_chr_expressions(code)
        
        # Шаг 3: Упрощение выражений с int()
        print("  Шаг 3: Упрощение выражений с int()...")
        code = simplify_int_expressions(code)
        
        # Шаг 4: Упрощение сложных выражений и конкатенаций строк
        print("  Шаг 4: Упрощение сложных выражений...")
        code = simplify_complex_expressions(code)
        
        # Шаг 5: Упрощение вызовов decode()
        print("  Шаг 5: Упрощение вызовов decode()...")
        code = simplify_decode_calls(code)
        
        # Шаг 6: Очистка вызовов getattr()
        print("  Шаг 6: Очистка вызовов getattr()...")
        code = clean_getattr_calls(code)
        
        # Шаг 7: Исправление строк
        print("  Шаг 7: Исправление проблем с кавычками в строках...")
        code = fix_string_quotes(code)
        code = fix_broken_strings(code)
        
        # Сохраняем промежуточный результат
        step_file = os.path.join('deobfuscation_steps', f"{output_prefix}_pass{i+1}.py")
        with open(step_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"  Результат прохода {i+1} сохранен в {step_file}")
        
        # Проверяем, изменился ли код после этого прохода
        if code == previous_code:
            print(f"  Код не изменился после прохода {i+1}, завершаем деобфускацию")
            break
    
    # Финальная очистка
    print("\nФинальная очистка кода...")
    code = cleanup_imports(code)
    
    # Сохраняем итоговый результат
    final_output = f"{output_prefix}_deobfuscated.py"
    with open(final_output, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\nДеобфускация завершена. Итоговый результат сохранен в {final_output}")
    print("""
Что делать дальше:
1. Проверить код на синтаксические ошибки
2. Вручную исправить оставшиеся проблемы
3. Переименовать переменные и функции для лучшей читаемости
4. Использовать форматирование кода для улучшения читаемости
""")

def main():
    if len(sys.argv) < 2:
        print("Использование: python final_decoder.py <input_file> [output_prefix] [--debug]")
        print("  --debug: Включить отладочные сообщения и комментарии в коде")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "layer10"
    debug_mode = "--debug" in sys.argv
    
    deobfuscate_file(input_file, output_prefix, debug=debug_mode)

if __name__ == "__main__":
    main() 