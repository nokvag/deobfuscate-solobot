#!/usr/bin/env python3

import re
import os
import string

# Ключ XOR, извлеченный из предыдущего слоя
XOR_KEY = [
    52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
    103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
    76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
    58, 48, 248, 136, 234, 128, 174, 58, 109, 129
]

def decode_xor_data(data, key=XOR_KEY):
    """
    Декодирует данные с использованием XOR и указанного ключа
    """
    if not key or not data:
        return data
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def fix_function_definitions(code):
    """
    Исправляет определения функций в коде
    """
    # Исправляем определение функции xor_decode
    xor_decode_fixed = """def xor_decode(data):
    # Декодирует данные, используя XOR-шифрование с ключом
    # Ключ XOR
    key = [
        52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
        103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
        76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
        58, 48, 248, 136, 234, 128, 174, 58, 109, 129
    ]
    
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
"""
    # Ищем и заменяем функцию xor_decode
    xor_decode_pattern = r'def xor_decode(?:data|data:).*?(?=def|\Z)'
    code = re.sub(xor_decode_pattern, xor_decode_fixed, code, flags=re.DOTALL)
    
    # Исправляем определение функции import_module
    import_module_fixed = """def import_module(var_1, var_2, *var_3, **var_4):
    try:
        return __import__(
            var_1 + "." + var_2,
            *var_3,
            **var_4,
        )
    except Exception:
        return __import__(var_1, *var_3, **var_4)
"""
    # Проверяем, есть ли функция import_module
    import_module_pattern = r'def import_module\(var_1, var_2, \*var_3, \*\*var_4\):.*?(?=def|\(asyncio|\Z)'
    if re.search(import_module_pattern, code, re.DOTALL):
        code = re.sub(import_module_pattern, import_module_fixed, code, flags=re.DOTALL)
    
    return code

def is_printable(s):
    """
    Проверяет, содержит ли строка только печатные символы
    """
    printable_chars = set(string.printable)
    return all(c in printable_chars for c in s)

def decode_byte_strings(code):
    """
    Декодирует байтовые строки в коде с использованием XOR-ключа
    """
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    
    def bytes_replacer(match):
        try:
            byte_str = match.group(1)
            # Очищаем строку от непечатаемых символов
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            
            # Пробуем преобразовать в байты
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Пробуем декодировать напрямую в UTF-8
            try:
                decoded_str = byte_data.decode('utf-8')
                if is_printable(decoded_str):
                    return f'"{decoded_str}"'
            except UnicodeDecodeError:
                pass
            
            # Декодируем с использованием XOR
            decoded_bytes = decode_xor_data(byte_data)
            try:
                decoded_str = decoded_bytes.decode('utf-8')
                if is_printable(decoded_str):
                    return f'"{decoded_str}"'
            except UnicodeDecodeError:
                pass
            
            # Если не удалось декодировать, возвращаем исходную строку
            return match.group(0)
        except Exception:
            return match.group(0)
    
    return re.sub(bytes_pattern, bytes_replacer, code)

def decode_unknown_calls(code):
    """
    Декодирует вызовы unknown_1(b'...') с использованием XOR-ключа
    """
    unknown_pattern = r'unknown_1\(b[\'"]([^\'"]*)[\'"](?:\s*\))+'
    
    def unknown_replacer(match):
        try:
            byte_str = match.group(1)
            # Очищаем строку от непечатаемых символов
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            
            # Пробуем преобразовать в байты
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Декодируем с использованием XOR
            decoded_bytes = decode_xor_data(byte_data)
            try:
                decoded_str = decoded_bytes.decode('utf-8')
                if is_printable(decoded_str):
                    return f'"{decoded_str}"'
            except UnicodeDecodeError:
                pass
            
            # Если не удалось декодировать, возвращаем исходную строку
            return match.group(0)
        except Exception:
            return match.group(0)
    
    return re.sub(unknown_pattern, unknown_replacer, code)

def fix_decode_calls(code):
    """
    Исправляет различные варианты вызовов decode
    """
    # Шаблон 1: X.decode if hasattr(Y, 'decode') else ("utf-8")
    pattern1 = r'([^\.]+)\.decode\s+if\s+hasattr\((?:[^,]+),\s*[\'"]decode[\'"]\)\s+else\s+\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern1, r'\1.decode("utf-8")', code)
    
    # Шаблон 2: getattr(X, "decode", )("utf-8")
    pattern2 = r'getattr\(([^,]+),\s*[\'"]decode[\'"],\s*(?:\s*\))?\s*\)\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern2, r'\1.decode("utf-8")', code)
    
    # Шаблон 3: "X".decode("utf-8")
    pattern3 = r'([\'"][^\'"]*[\'"])\.decode\([\'"]utf-8[\'"]\)'
    code = re.sub(pattern3, r'\1', code)
    
    return code

def fix_syntax_errors(code):
    """
    Исправляет различные синтаксические ошибки в коде
    """
    # Исправляем if __name__ == ...
    code = re.sub(r'if __name__ == getattr\(b\'_D[^\']*\', "decode",\s*\)\([\'"]utf-8[\'"]\):', 
                 'if __name__ == "__main__":', code)
    
    # Исправляем странные конструкции вроде )name(
    code = re.sub(r'\)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', r').\1(', code)
    
    # Исправляем конструкции вида )name
    code = re.sub(r'\)\s*([a-zA-Z_][a-zA-Z0-9_]*)', r').\1', code)
    
    # Исправляем ошибки с пробелами в вызовах методов
    code = re.sub(r'\.([a-zA-Z_][a-zA-Z0-9_]*)\s+\(', r'.\1(', code)
    
    # Исправляем отсутствие разделителей в вызовах
    code = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\)\(', r'\1).(', code)
    
    # Исправляем отсутствие разделителей перед аргументами
    code = re.sub(r'\)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?!\()', r', \1', code)
    
    return code

def improve_readability(code):
    """
    Улучшает читаемость кода
    """
    # Заменяем странные шаблоны использования getattr
    pattern = r'getattr\(([^,]+),\s*([\'"][^\'"]*[\'"])\s*(?:,\s*[^,]*\s*)?\)'
    
    def getattr_replacer(match):
        obj = match.group(1).strip()
        attr = match.group(2).strip()
        
        # Извлекаем строку атрибута из кавычек
        if attr.startswith('"') and attr.endswith('"'):
            attr = attr[1:-1]
        elif attr.startswith("'") and attr.endswith("'"):
            attr = attr[1:-1]
        else:
            return match.group(0)
        
        # Проверяем, является ли атрибут допустимым идентификатором
        if all(c.isalnum() or c == '_' for c in attr) and not attr[0].isdigit():
            return f"{obj}.{attr}"
        else:
            return match.group(0)
    
    return re.sub(pattern, getattr_replacer, code)

def remove_extra_parentheses(code):
    """
    Удаляет лишние скобки
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
        'var_25': 'check_interval',
        'var_29': 'handle_template',
        'var_31': 'command_handler',
        'var_33': 'metrics_handler',
        'var_35': 'oauth_handler',
        'var_36': 'auth_handler',
        'var_37': 'logger',
        'var_38': 'periodic_task',
        'var_51': 'task',
        'var_53': 'site',
        'var_56': 'tasks',
        'var_62': 'runner',
        'var_63': 'event',
        'var_64': 'signal_handler',
    }
    
    # Заменяем имена переменных
    for old_name, new_name in var_mappings.items():
        code = re.sub(r'\b' + old_name + r'\b', new_name, code)
    
    return code

def fix_f_strings(code):
    """
    Исправляет f-строки, которые были неправильно записаны
    """
    # Находим строки вида "URL вебхука: {webhook_url}" и преобразуем их в f-строки
    pattern = r'[\'"]([^\'"]*)(\{[a-zA-Z_][a-zA-Z0-9_]*\})([^\'"]*)[\'"]'
    
    def f_string_replacer(match):
        prefix = match.group(1)
        var = match.group(2)
        suffix = match.group(3)
        delimiter = match.group(0)[0]  # ' или "
        return f'f{delimiter}{prefix}{var}{suffix}{delimiter}'
    
    return re.sub(pattern, f_string_replacer, code)

def deobfuscate_layer12(input_file, output_file):
    """
    Основная функция деобфускации layer12.py
    """
    # Загружаем код из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Исходный размер файла: {original_size} байт")
    
    # Шаг 1: Исправляем определения функций
    print("Исправление определений функций...")
    code = fix_function_definitions(code)
    
    # Шаг 2: Декодируем байтовые строки
    print("Декодирование байтовых строк...")
    code = decode_byte_strings(code)
    
    # Шаг 3: Декодируем вызовы unknown_1
    print("Декодирование вызовов unknown_1()...")
    code = decode_unknown_calls(code)
    
    # Шаг 4: Исправляем вызовы decode
    print("Исправление вызовов decode()...")
    code = fix_decode_calls(code)
    
    # Шаг 5: Исправляем синтаксические ошибки
    print("Исправление синтаксических ошибок...")
    code = fix_syntax_errors(code)
    
    # Шаг 6: Улучшаем читаемость кода
    print("Улучшение читаемости кода...")
    code = improve_readability(code)
    
    # Шаг 7: Удаляем лишние скобки
    print("Удаление лишних скобок...")
    code = remove_extra_parentheses(code)
    
    # Шаг 8: Переименовываем переменные
    print("Переименование переменных...")
    code = rename_variables(code)
    
    # Шаг 9: Исправляем f-строки
    print("Исправление f-строк...")
    code = fix_f_strings(code)
    
    # Сохраняем деобфусцированный код
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Новый размер файла: {new_size} байт")
    print(f"Разница: {new_size - original_size:+d} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer12("layer12.py", "layer13.py") 