#!/usr/bin/env python3

import re
import os
import builtins
import keyword
import string

def extract_xor_key(code):
    """
    Извлекает ключ XOR из функции xor_decode
    """
    xor_decode_func_pattern = r'def xor_decode\(data\):(.*?)(?=def|\Z)'
    xor_decode_func_match = re.search(xor_decode_func_pattern, code, re.DOTALL)
    
    if xor_decode_func_match:
        xor_decode_func_body = xor_decode_func_match.group(1).strip()
        
        # Ищем определение ключа
        xor_key_pattern = r'key = \[([\d, \n]+)\]'
        xor_key_match = re.search(xor_key_pattern, xor_decode_func_body, re.DOTALL)
        
        if xor_key_match:
            key_str = xor_key_match.group(1).replace('\n', '').replace(' ', '')
            try:
                xor_key = eval(f"[{key_str}]")
                return xor_key
            except Exception as e:
                print(f"Ошибка при извлечении ключа XOR: {e}")
    
    return None

def decode_xor_data(data, key):
    """
    Декодирует данные с использованием XOR и указанного ключа
    """
    if not key or not data:
        return data
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def xor_decode_function():
    """
    Возвращает правильную функцию xor_decode
    """
    return """def xor_decode(data):
    # Декодирует данные, используя XOR-шифрование с ключом
    # Ключ XOR (был извлечен из оригинальной функции)
    key = [
        52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
        103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
        76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
        58, 48, 248, 136, 234, 128, 174, 58, 109, 129
    ]
    
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
"""

def import_module_function():
    """
    Возвращает правильную функцию import_module
    """
    return """def import_module(var_1, var_2, *var_3, **var_4):
    try:
        return __import__(
            var_1
            + "."
            + var_2,
            *var_3,
            **var_4,
        )
    except Exception:
        return __import__(var_1, *var_3, **var_4)
"""

def decode_bytes_with_xor(code, xor_key):
    """
    Декодирует все байтовые строки в коде с использованием XOR-ключа
    """
    if not xor_key:
        return code
    
    # Шаблон для байтовых строк
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    
    # Словарь для хранения декодированных строк
    decoded_strings = {}
    
    # Находим все байтовые строки
    byte_matches = re.findall(bytes_pattern, code)
    
    # Декодируем каждую байтовую строку
    for byte_str in byte_matches:
        try:
            # Очищаем строку от непечатаемых символов
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            # Преобразуем в байты
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Пробуем декодировать напрямую
            try:
                decoded_str = byte_data.decode('utf-8')
                # Если в строке только печатаемые символы, то считаем, что это уже декодированная строка
                if all(c in string.printable for c in decoded_str):
                    decoded_strings[f"b'{byte_str}'"] = f'"{decoded_str}"'
                    decoded_strings[f'b"{byte_str}"'] = f'"{decoded_str}"'
                    continue
            except UnicodeDecodeError:
                pass
            
            # Декодируем с использованием XOR
            decoded_bytes = decode_xor_data(byte_data, xor_key)
            try:
                # Пробуем преобразовать в строку
                decoded_str = decoded_bytes.decode('utf-8')
                
                # Проверяем, что строка содержит только печатаемые символы
                if all(c in string.printable for c in decoded_str):
                    decoded_strings[f"b'{byte_str}'"] = f'"{decoded_str}"'
                    decoded_strings[f'b"{byte_str}"'] = f'"{decoded_str}"'
            except UnicodeDecodeError:
                pass
        except Exception as e:
            # Если произошла ошибка, пропускаем эту строку
            continue
    
    # Заменяем все закодированные строки на декодированные
    for original, decoded in decoded_strings.items():
        code = code.replace(original, decoded)
    
    return code

def decode_unknown_calls(code, xor_key):
    """
    Декодирует все вызовы unknown_1(b'...') в коде
    """
    if not xor_key:
        return code
    
    # Шаблон для вызовов unknown_1
    unknown_pattern = r'unknown_1\(b[\'"]([^\'"]*)[\'"](?:\s*\))+'
    
    # Находим все вызовы unknown_1
    unknown_matches = re.findall(unknown_pattern, code)
    
    # Декодируем каждый найденный вызов
    for byte_str in unknown_matches:
        try:
            # Очищаем строку от непечатаемых символов
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            # Преобразуем в байты
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Декодируем с использованием XOR
            decoded_bytes = decode_xor_data(byte_data, xor_key)
            try:
                # Пробуем преобразовать в строку
                decoded_str = decoded_bytes.decode('utf-8')
                
                # Проверяем, что строка содержит только печатаемые символы
                if all(c in string.printable for c in decoded_str):
                    # Заменяем вызов на декодированную строку
                    code = code.replace(f"unknown_1(b'{byte_str}')", f'"{decoded_str}"')
                    code = code.replace(f'unknown_1(b"{byte_str}")', f'"{decoded_str}"')
            except UnicodeDecodeError:
                pass
        except Exception as e:
            # Если произошла ошибка, пропускаем эту строку
            continue
    
    return code

def clean_getattr_decode_calls(code):
    """
    Очищает различные формы вызовов getattr для методов decode
    """
    # Шаблон 1: getattr(X, "decode", )("utf-8")
    pattern1 = r'getattr\(([^,]+),\s*[\'"]decode[\'"],\s*(?:\s*\))?\s*\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern1, lambda m: f'{m.group(1)}.decode("utf-8")', code)
    
    # Шаблон 2: X.decode("utf-8")
    pattern2 = r'([\'"][^\'"]*[\'"])\.decode\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern2, lambda m: m.group(1), code)
    
    # Шаблон 3: bizarre syntax with hasattr
    pattern3 = r'([^\.]+)\.decode if hasattr\([^,]+, [\'"]decode[\'"]\) else\s*\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern3, lambda m: f'{m.group(1)}', code)
    
    return code

def simplify_getattr_calls(code):
    """
    Упрощает вызовы getattr(obj, "attr") на obj.attr
    """
    getattr_pattern = r'getattr\(([^,]+),\s*[\'"]([^\'"]+)[\'"](?:\s*\))+'
    
    def replacer(match):
        obj = match.group(1).strip()
        attr = match.group(2).strip()
        
        # Проверяем, что атрибут является допустимым идентификатором
        if attr.isidentifier() and not keyword.iskeyword(attr):
            return f"{obj}.{attr}"
        else:
            return match.group(0)
    
    return re.sub(getattr_pattern, replacer, code)

def fix_imports(code):
    """
    Исправляет и упрощает импорты
    """
    # Заменяем [encoded].decode на "encoded"
    code = re.sub(r'\[encoded\]\.decode', r'"encoded"', code)
    
    # Исправляем синтаксические ошибки в импортах
    code = re.sub(r'if hasattr\(import_module\(\s*"encoded"\s*\)', 
                  r'if hasattr(import_module("encoded"), "decode")', code)
    
    return code

def fix_syntax_errors(code):
    """
    Исправляет различные синтаксические ошибки в коде
    """
    # Исправляем except all: на except Exception:
    code = re.sub(r'except all:', r'except Exception:', code)
    
    # Исправляем неправильные вызовы функций
    code = re.sub(r'__import__\(\s*([^,]+)\s*\+\s*"\."\s*\+\s*([^,]+)', 
                  r'__import__(\1 + "." + \2', code)
    
    # Заменяем неправильные выражения hasattr
    code = re.sub(r'hasattr\(([^,]+), \'decode\'\)', r'hasattr(\1, "decode")', code)
    
    return code

def clean_multiple_parentheses(code):
    """
    Удаляет лишние скобки и упрощает сложные выражения
    """
    # Удаляем лишние скобки вокруг идентификаторов
    code = re.sub(r'\(([a-zA-Z_][a-zA-Z0-9_]*)\)', r'\1', code)
    
    # Удаляем лишние скобки вокруг строковых литералов
    code = re.sub(r'\(([\'"][^\'"]*[\'"])\)', r'\1', code)
    
    return code

def rename_variables(code):
    """
    Переименовывает переменные var_X на более осмысленные имена
    """
    # Словарь для переименования переменных
    var_mappings = {
        'var_6': 'signal',
        'var_7': 'register_webapps',
        'var_8': 'webapps_manager',
        'var_11': 'bot',
        'var_12': 'dp',
        'var_13': 'periodic_task_interval',
        'var_14': 'handle_commands',
        'var_15': 'use_webhook',
        'var_16': 'use_custom_templates',
        'var_17': 'process_metrics',
        'var_18': 'base_url',
        'var_19': 'host',
        'var_20': 'port',
        'var_21': 'bot_path',
        'var_22': 'webhook_url',
        'var_23': 'handle_oauth',
        'var_24': 'handle_auth',
        'var_25': 'check_interval'
    }
    
    # Заменяем имена переменных
    for old_name, new_name in var_mappings.items():
        code = re.sub(r'\b' + old_name + r'\b', new_name, code)
    
    return code

def fix_xor_decode_function(code):
    """
    Полностью заменяет функцию xor_decode на правильную версию
    """
    # Ищем функцию xor_decode в коде
    xor_decode_pattern = r'def xor_decode\(data\):[^}]*?(?=def|\Z)'
    xor_decode_match = re.search(xor_decode_pattern, code, re.DOTALL)
    
    if xor_decode_match:
        # Заменяем функцию на правильную версию
        code = code.replace(xor_decode_match.group(0), xor_decode_function())
    
    return code

def fix_import_module_function(code):
    """
    Полностью заменяет функцию import_module на правильную версию
    """
    # Ищем функцию import_module в коде
    import_module_pattern = r'def import_module\(var_1, var_2, \*var_3, \*\*var_4\):[^}]*?(?=def|\Z)'
    import_module_match = re.search(import_module_pattern, code, re.DOTALL)
    
    if import_module_match:
        # Заменяем функцию на правильную версию
        code = code.replace(import_module_match.group(0), import_module_function())
    
    return code

def deobfuscate_layer11_final(input_file, output_file):
    """
    Основная функция финальной деобфускации слоя 11
    """
    # Загружаем код из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Исходный размер файла: {original_size} байт")
    
    # Извлекаем ключ XOR
    print("Извлечение ключа XOR...")
    xor_key = extract_xor_key(code)
    if xor_key:
        print(f"Ключ XOR: {xor_key}")
    else:
        print("Не удалось извлечь ключ XOR")
        xor_key = [52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 58, 48, 248, 136, 234, 128, 174, 58, 109, 129]
        print(f"Используем предопределенный ключ XOR: {xor_key}")
    
    # Применяем функции деобфускации
    print("Исправление функции xor_decode...")
    code = fix_xor_decode_function(code)
    
    print("Исправление функции import_module...")
    code = fix_import_module_function(code)
    
    print("Декодирование всех байтовых строк с использованием XOR...")
    code = decode_bytes_with_xor(code, xor_key)
    
    print("Декодирование вызовов unknown_1()...")
    code = decode_unknown_calls(code, xor_key)
    
    print("Очистка вызовов decode('utf-8')...")
    code = clean_getattr_decode_calls(code)
    
    print("Упрощение вызовов getattr()...")
    code = simplify_getattr_calls(code)
    
    print("Исправление импортов...")
    code = fix_imports(code)
    
    print("Исправление синтаксических ошибок...")
    code = fix_syntax_errors(code)
    
    print("Удаление лишних скобок...")
    code = clean_multiple_parentheses(code)
    
    print("Переименование переменных...")
    code = rename_variables(code)
    
    # Сохраняем деобфусцированный код
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Новый размер файла: {new_size} байт")
    print(f"Разница: {new_size - original_size} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer11_final("layer11.py", "layer12_final.py") 