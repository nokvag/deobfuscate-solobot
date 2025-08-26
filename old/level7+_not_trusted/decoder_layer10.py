#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import ast
import astunparse
from typing import ByteString, Union

# Оригинальный ключ из layer10.py
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

def decode_original(obj, *a, **kw):
    """Исходная функция decode из layer10.py"""
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj

def replace_chr_expressions(code: str) -> str:
    """Заменяет сложные выражения с chr() на их значения"""
    def chr_replacer(match):
        expr = match.group(1)
        try:
            value = eval(expr)
            return f'"{chr(value)}"'
        except:
            return match.group(0)
    
    # Заменяем выражения вида chr(117) или chr(1000 - 884)
    pattern = r'chr\((.*?)\)'
    return re.sub(pattern, chr_replacer, code)

def replace_xor_transform_calls(code: str) -> str:
    """Заменяет вызовы xor_transform() на их расшифрованные значения"""
    pattern = r'xor_transform\(\s*b([\'"])(.*?)(\1)\s*\)'
    
    def replacer(match):
        quote = match.group(1)
        raw_bytes_str = match.group(2)
        
        try:
            # Преобразуем строку в байты для расшифровки
            raw_bytes = eval(f"b{quote}{raw_bytes_str}{quote}")
            decrypted = xor_transform(raw_bytes)
            decoded_text = decrypted.decode('utf-8', errors='replace')
            return f'"{decoded_text}"'
        except Exception as e:
            return f'/* Ошибка расшифровки: {e} */ {match.group(0)}'
    
    return re.sub(pattern, replacer, code)

def simplify_decode_calls(code: str) -> str:
    """Упрощает вызовы функции decode() с конкатенацией строк"""
    # Паттерн для поиска decode('u' + 't' + 'f' + '-' + '8')
    pattern = r'decode\(((?:[\'"][^\'\"]*[\'"](?:\s*\+\s*)?)+)\)'
    
    def decode_replacer(match):
        concat_expr = match.group(1)
        try:
            # Вычисляем конкатенацию строк
            value = eval(concat_expr)
            return f'"{value}"'
        except:
            return match.group(0)
    
    return re.sub(pattern, decode_replacer, code)

def simplify_getattr_calls(code: str) -> str:
    """Упрощает вызовы getattr(obj, 'method')() в obj.method()"""
    pattern = r'getattr\(([^,]+),\s*([^)]+)\)'
    
    def getattr_replacer(match):
        obj = match.group(1).strip()
        attr = match.group(2).strip()
        
        # Если атрибут - строковый литерал, можем упростить
        if (attr.startswith('"') and attr.endswith('"')) or (attr.startswith("'") and attr.endswith("'")):
            attr_value = attr[1:-1]  # Убираем кавычки
            return f"{obj}.{attr_value}"
        # Если это вызов decode, попробуем вычислить
        elif attr.startswith('decode('):
            return match.group(0)  # Пока оставляем как есть
        else:
            return match.group(0)
    
    return re.sub(pattern, getattr_replacer, code)

def replace_int_expressions(code: str) -> str:
    """Заменяет сложные выражения с int() на их значения"""
    # Паттерн для поиска int('0' + 'o' + '1', 8) и подобных
    pattern = r'int\(((?:[\'"][^\'\"]*[\'"](?:\s*\+\s*)?)+),\s*(\d+)\)'
    
    def int_replacer(match):
        concat_expr = match.group(1)
        base = int(match.group(2))
        
        try:
            # Вычисляем выражение внутри int()
            value_str = eval(concat_expr)
            value = int(value_str, base)
            return str(value)
        except:
            return match.group(0)
    
    return re.sub(pattern, int_replacer, code)

def simplify_arithmetic_expressions(code: str) -> str:
    """Упрощает арифметические выражения в строках"""
    # Паттерн для поиска выражений вида (1000 - 884) или (0b1000 + 0o154)
    patterns = [
        (r'\((\d+)\s*([+\-*])\s*(\d+)\)', r'(\1 \2 \3)'),  # Простые арифметические выражения
        (r'\(0[boxBOX]\w+\s*([+\-*])\s*0[boxBOX]\w+\)', r'(\1 \2 \3)')  # Выражения с разными системами счисления
    ]
    
    def eval_expr(match):
        try:
            expr = match.group(0)
            value = eval(expr)
            return str(value)
        except:
            return match.group(0)
    
    # Применяем паттерны последовательно
    result = code
    for pattern, _ in patterns:
        result = re.sub(pattern, eval_expr, result)
    
    return result

def rename_obfuscated_variables(code: str) -> str:
    """Переименовывает обфусцированные переменные в более читаемые имена"""
    # Находим переменные с обфусцированными именами (много согласных подряд, смесь верхнего и нижнего регистра)
    pattern = r'\b([a-zA-Z][a-zA-Z0-9_]{5,})\b'
    
    obfuscated_vars = {}
    counter = 1
    
    def is_likely_obfuscated(var_name):
        # Проверка, похоже ли имя на обфусцированное
        if len(var_name) < 6:
            return False
        
        # Если имя содержит подчеркивания и смесь верхнего и нижнего регистра
        has_upper = any(c.isupper() for c in var_name)
        has_lower = any(c.islower() for c in var_name)
        has_underscore = '_' in var_name
        has_digits = any(c.isdigit() for c in var_name)
        
        if (has_upper and has_lower and (has_underscore or has_digits)):
            return True
        
        return False
    
    def var_replacer(match):
        nonlocal counter
        var_name = match.group(0)
        
        # Пропускаем стандартные имена и функции
        if var_name in ['decode', 'getattr', 'isinstance', 'enumerate', 'xor_transform', 'bytearray',
                        'bytes', 'TypeError', 'Exception', 'print', 'open', 'globals', 'locals',
                        'int', 'str', 'chr', 'eval', '__import__', '__name__', 'import_module']:
            return var_name
        
        if is_likely_obfuscated(var_name) and var_name not in obfuscated_vars:
            obfuscated_vars[var_name] = f"deobf_var_{counter}"
            counter += 1
        
        return obfuscated_vars.get(var_name, var_name)
    
    return re.sub(pattern, var_replacer, code)

def simplify_string_concatenation(code: str) -> str:
    """Упрощает конкатенацию строк"""
    # Паттерн для поиска конкатенации строк 'a' + 'b' + 'c'
    pattern = r'((?:[\'"][^\'\"]*[\'"](?:\s*\+\s*)?)+)'
    
    def concat_replacer(match):
        concat_expr = match.group(1)
        # Проверяем, что это действительно конкатенация (содержит +)
        if '+' in concat_expr:
            try:
                value = eval(concat_expr)
                return f'"{value}"'
            except:
                return match.group(0)
        return match.group(0)
    
    return re.sub(pattern, concat_replacer, code)

def simplify_hex_oct_bin_literals(code: str) -> str:
    """Преобразует шестнадцатеричные, восьмеричные и двоичные литералы в десятичные"""
    # Находим литералы вида 0x123, 0o123, 0b101
    pattern = r'\b(0[xXoObB][0-9a-fA-F]+)\b'
    
    def literal_replacer(match):
        literal_str = match.group(1)
        try:
            value = eval(literal_str)
            return str(value)
        except:
            return match.group(0)
    
    return re.sub(pattern, literal_replacer, code)

def cleanup_imports(code: str) -> str:
    """Удаляет дублирующиеся и неиспользуемые импорты"""
    # Очень упрощенная версия - просто находим и удаляем очевидные дублирования
    lines = code.split('\n')
    imports = set()
    result = []
    
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            if line.strip() not in imports:
                imports.add(line.strip())
                result.append(line)
        else:
            result.append(line)
    
    return '\n'.join(result)

def extract_string_literals(code: str):
    """Извлекает строковые литералы для последующего анализа и декодирования"""
    # Паттерн для строковых литералов
    pattern = r'([\'"])((?:\\\1|.)*?)\1'
    
    strings = []
    for match in re.finditer(pattern, code):
        strings.append(match.group(2))
    
    return strings

def replace_patches_calls(code: str) -> str:
    """Упрощает вызовы patches()"""
    pattern = r'patches\((.*?)\)'
    
    def patches_replacer(match):
        args = match.group(1)
        if "utf-8" in args:
            return "importlib.import_module('utf-8')"
        return match.group(0)
    
    return re.sub(pattern, patches_replacer, code)

def deobfuscate_layer10_multi_pass(input_file: str, output_file: str, passes: int = 3):
    """Многопроходная деобфускация файла layer10.py"""
    print(f"Начинаю многопроходную деобфускацию файла {input_file}...")
    
    # Чтение содержимого файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Сохранение оригинального кода
    original_code = code
    
    # Многопроходная деобфускация
    for pass_num in range(1, passes + 1):
        print(f"\nПроход {pass_num}/{passes}:")
        
        # Шаг 1: Расшифровываем вызовы xor_transform
        print("Шаг 1: Расшифровка вызовов xor_transform...")
        code = replace_xor_transform_calls(code)
        
        # Шаг 2: Упрощаем выражения с chr()
        print("Шаг 2: Упрощение выражений с chr()...")
        code = replace_chr_expressions(code)
        
        # Шаг 3: Упрощаем вызовы decode
        print("Шаг 3: Упрощение вызовов decode...")
        code = simplify_decode_calls(code)
        
        # Шаг 4: Упрощаем getattr вызовы
        print("Шаг 4: Упрощение getattr вызовов...")
        code = simplify_getattr_calls(code)
        
        # Шаг 5: Упрощаем выражения с int()
        print("Шаг 5: Упрощение выражений с int()...")
        code = replace_int_expressions(code)
        
        # Шаг 6: Упрощаем арифметические выражения
        print("Шаг 6: Упрощение арифметических выражений...")
        code = simplify_arithmetic_expressions(code)
        
        # Шаг 7: Упрощаем конкатенацию строк
        print("Шаг 7: Упрощение конкатенации строк...")
        code = simplify_string_concatenation(code)
        
        # Шаг 8: Упрощаем литералы различных систем счисления
        print("Шаг 8: Упрощение литералов различных систем счисления...")
        code = simplify_hex_oct_bin_literals(code)
        
        # Шаг 9: Упрощаем вызовы patches
        print("Шаг 9: Упрощение вызовов patches...")
        code = replace_patches_calls(code)
        
        # Запись промежуточного результата
        intermediate_file = f"{output_file.rsplit('.', 1)[0]}_pass{pass_num}.py"
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Результат прохода {pass_num} сохранен в {intermediate_file}")
        
        # Проверка на изменения в коде
        if code == original_code:
            print(f"Код не изменился после прохода {pass_num}. Завершаем деобфускацию.")
            break
        
        original_code = code
    
    # Шаг 10: Очистка импортов (опционально)
    print("\nШаг 10: Очистка импортов...")
    code = cleanup_imports(code)
    
    # Шаг 11: Переименование обфусцированных переменных (опционально)
    print("Шаг 11: Переименование обфусцированных переменных...")
    # Раскомментируйте следующую строку для переименования переменных
    # code = rename_obfuscated_variables(code)
    
    # Запись финального результата
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\nДеобфускация завершена. Итоговый результат сохранен в {output_file}")
    print("\nДля дополнительной очистки кода рекомендуется:")
    print("1. Использовать инструменты форматирования кода (black, autopep8)")
    print("2. Вручную проанализировать оставшиеся сложные выражения")
    print("3. При необходимости упростить логику программы")
    print("4. Проверить и исправить потенциальные ошибки синтаксиса")

def deobfuscate_layer10(input_file: str, output_file: str):
    """Основная функция деобфускации файла layer10.py (однопроходная)"""
    print(f"Начинаю деобфускацию файла {input_file}...")
    
    # Чтение содержимого файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Шаг 1: Расшифровываем вызовы xor_transform
    print("Шаг 1: Расшифровка вызовов xor_transform...")
    code = replace_xor_transform_calls(code)
    
    # Шаг 2: Упрощаем выражения с chr()
    print("Шаг 2: Упрощение выражений с chr()...")
    code = replace_chr_expressions(code)
    
    # Шаг 3: Упрощаем вызовы decode
    print("Шаг 3: Упрощение вызовов decode...")
    code = simplify_decode_calls(code)
    
    # Шаг 4: Упрощаем getattr вызовы
    print("Шаг 4: Упрощение getattr вызовов...")
    code = simplify_getattr_calls(code)
    
    # Шаг 5: Упрощаем выражения с int()
    print("Шаг 5: Упрощение выражений с int()...")
    code = replace_int_expressions(code)
    
    # Шаг 6: Упрощаем арифметические выражения
    print("Шаг 6: Упрощение арифметических выражений...")
    code = simplify_arithmetic_expressions(code)
    
    # Шаг 7: Переименовываем обфусцированные переменные (опционально)
    print("Шаг 7: Переименование обфусцированных переменных...")
    # code = rename_obfuscated_variables(code)  # Раскомментируйте эту строку для переименования переменных
    
    # Запись промежуточного результата
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Шаг 8: Форматирование кода (опционально)
    print("Шаг 8: Форматирование кода...")
    # Здесь можно добавить форматирование с использованием black или autopep8
    
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")
    print("Для дополнительной очистки кода рекомендуется:")
    print("1. Использовать инструменты форматирования кода (black, autopep8)")
    print("2. Вручную проанализировать оставшиеся сложные выражения")
    print("3. При необходимости упростить логику программы")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python decoder_layer10.py <путь_к_layer10.py> [выходной_файл] [--multi-pass]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "layer10_deobfuscated.py"
    
    use_multi_pass = '--multi-pass' in sys.argv
    
    if use_multi_pass:
        deobfuscate_layer10_multi_pass(input_file, output_file)
    else:
        deobfuscate_layer10(input_file, output_file) 