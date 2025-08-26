#!/usr/bin/env python3

import re
import ast
import os
import builtins
import keyword

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
    if not key:
        return data
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def fix_xor_decode_function(code):
    """
    Исправляет синтаксические ошибки в функции xor_decode
    """
    pattern = r'def xor_decode(data|data:)(.*?)(def|\Z)'
    
    def replacer(match):
        prefix = match.group(1)
        body = match.group(2)
        suffix = match.group(3)
        
        # Исправляем синтаксические ошибки в сигнатуре функции
        if prefix == 'data:' or prefix == 'data':
            fixed_prefix = '(data):'
        else:
            fixed_prefix = prefix
        
        # Исправляем ошибки в теле функции
        fixed_body = body.replace('lenkey', 'len(key)')
        fixed_body = fixed_body.replace('enumeratedata', 'enumerate(data)')
        
        return f'def xor_decode{fixed_prefix}{fixed_body}{suffix}'
    
    return re.sub(pattern, replacer, code, flags=re.DOTALL)

def decode_all_strings(code, xor_key):
    """
    Декодирует все зашифрованные строки в коде
    """
    if not xor_key:
        print("Не удалось использовать ключ XOR, продолжаем без него")
    
    # Декодируем вызовы b'...'
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    
    def bytes_replacer(match):
        try:
            byte_str = match.group(1)
            # Заменяем проблемные не-ASCII символы на их hex эквиваленты
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Пробуем декодировать как utf-8
            try:
                decoded_str = byte_data.decode('utf-8')
                # Если строка выглядит как бинарный мусор, пробуем XOR
                if any(c not in printable_chars for c in decoded_str) and xor_key:
                    raise UnicodeDecodeError("utf-8", b"", 0, 1, "Forcing XOR decoding")
                
                return f'"{decoded_str}"'
            except UnicodeDecodeError:
                # Если не удалось декодировать напрямую и у нас есть ключ XOR, пробуем через XOR
                if xor_key:
                    try:
                        decoded_bytes = decode_xor_data(byte_data, xor_key)
                        decoded_str = decoded_bytes.decode('utf-8')
                        return f'"{decoded_str}"'
                    except UnicodeDecodeError:
                        pass
                
                # Если не удалось декодировать, возвращаем оригинальное выражение
                return match.group(0)
        except Exception as e:
            # В случае ошибки возвращаем оригинальное выражение
            return match.group(0)
    
    # Заменяем все байтовые литералы
    code = re.sub(bytes_pattern, bytes_replacer, code)
    
    # Декодируем вызовы unknown_1(b'...')
    unknown_pattern = r'unknown_1\(b[\'"]([^\'"]*)[\'"](?:\s*\))?'
    
    def unknown_replacer(match):
        try:
            byte_str = match.group(1)
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            byte_data = eval(f"b'{cleaned_bytes}'")
            
            # Если у нас есть ключ XOR, применяем его
            if xor_key:
                try:
                    decoded_bytes = decode_xor_data(byte_data, xor_key)
                    decoded_str = decoded_bytes.decode('utf-8')
                    return f'"{decoded_str}"'
                except UnicodeDecodeError:
                    pass
            
            # Если декодирование не удалось или нет ключа XOR, возвращаем оригинальное выражение
            return match.group(0)
        except Exception as e:
            # В случае ошибки возвращаем оригинальное выражение
            return match.group(0)
    
    # Заменяем вызовы unknown_1
    code = re.sub(unknown_pattern, unknown_replacer, code)
    
    return code

def clean_decode_calls(code):
    """
    Очищает вызовы decode('utf-8')
    """
    # Заменяем сложные выражения для выполнения decode('utf-8')
    patterns = [
        # Шаблон 1: getattr(X, "decode", )('utf-8')
        (r'getattr\(([^,]+),\s*[\'"]decode[\'"],\s*\)\([\'"]utf-8[\'"]\)', lambda m: 
         f'{m.group(1)}.decode("utf-8")' if not (m.group(1).startswith('"') and m.group(1).endswith('"')) else 
         m.group(1)
        ),
        # Шаблон 2: X.decode('utf-8')
        (r'([\'"][^\'"]*[\'"])\.decode\([\'"]utf-8[\'"]\)', lambda m: m.group(1)),
        # Шаблон 3: X.decode if hasattr(X, 'decode') else ('utf-8')
        (r'([^\.]+)\.decode if hasattr\([^,]+, [\'"]decode[\'"]\) else\s*\([\'"]utf-8[\'"]\)', 
         lambda m: f'{m.group(1)}.decode("utf-8")'),
    ]
    
    for pattern, replacer in patterns:
        code = re.sub(pattern, replacer, code)
    
    return code

def simplify_getattr_calls(code):
    """
    Упрощает вызовы getattr на прямые обращения к атрибутам
    """
    # Ищем вызовы getattr с двумя аргументами (объект и имя атрибута в виде строки)
    getattr_pattern = r'getattr\(([^,]+),\s*([\'"][^\'"]*[\'"])\s*\)'
    
    def getattr_replacer(match):
        try:
            obj = match.group(1).strip()
            attr = match.group(2).strip()
            
            # Извлекаем строку атрибута из кавычек
            if attr.startswith('"') and attr.endswith('"'):
                attr = attr[1:-1]
            elif attr.startswith("'") and attr.endswith("'"):
                attr = attr[1:-1]
            else:
                # Если атрибут не является простой строкой, оставляем вызов как есть
                return match.group(0)
            
            # Проверяем, является ли атрибут допустимым идентификатором
            if attr.isidentifier() and not keyword.iskeyword(attr):
                return f"{obj}.{attr}"
            else:
                return match.group(0)
        except Exception:
            return match.group(0)
    
    code = re.sub(getattr_pattern, getattr_replacer, code)
    
    return code

def cleanup_imports(code):
    """
    Очищает импорты и исправляет синтаксические ошибки
    """
    # Исправляем синтаксические ошибки в импортах
    code = re.sub(r'import_module\(\s*\[encoded\]\.decode', r'import_module("encoded"', code)
    
    # Заменяем import_module на простые импорты, где возможно
    # Это требует более сложного анализа и может быть реализовано позднее
    
    return code

def fix_syntax_errors(code):
    """
    Исправляет синтаксические ошибки в коде
    """
    # Исправляем ошибки в операторах if
    code = re.sub(r'if hasattr\(import_module\(\s*\[encoded\]\.decode\)', 
                  r'if hasattr(import_module("encoded"), "decode")', code)
    
    # Исправляем другие синтаксические ошибки
    code = re.sub(r'except all:', r'except Exception:', code)
    
    return code

def extract_and_decode_strings(code, xor_key):
    """
    Ищет и декодирует все строки в коде, закодированные с помощью XOR
    """
    if not xor_key:
        return code
    
    # Находим все строковые литералы
    string_pattern = r'[\'"]([^\'"]*)[\'"]'
    byte_string_pattern = r'b[\'"]([^\'"]*)[\'"]'
    
    # Собираем все строки для проверки
    strings = re.findall(string_pattern, code)
    byte_strings = re.findall(byte_string_pattern, code)
    
    # Пытаемся декодировать каждую байтовую строку
    decoded_strings = {}
    for byte_str in byte_strings:
        try:
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
            byte_data = eval(f"b'{cleaned_bytes}'")
            decoded_bytes = decode_xor_data(byte_data, xor_key)
            decoded_str = decoded_bytes.decode('utf-8')
            
            # Проверяем, что декодированная строка имеет смысл (например, содержит только печатные символы)
            if is_printable(decoded_str):
                decoded_strings[f"b'{byte_str}'"] = f'"{decoded_str}"'
                decoded_strings[f'b"{byte_str}"'] = f'"{decoded_str}"'
        except Exception:
            continue
    
    # Заменяем все найденные и декодированные строки
    for original, decoded in decoded_strings.items():
        code = code.replace(original, decoded)
    
    return code

def is_printable(s):
    """
    Проверяет, содержит ли строка только печатные символы
    """
    printable_chars = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r")
    return all(c in printable_chars for c in s)

def simplify_code_structures(code):
    """
    Упрощает различные структуры кода
    """
    # Удаляем лишние скобки
    code = re.sub(r'\(([a-zA-Z_][a-zA-Z0-9_]*)\)', r'\1', code)
    
    # Упрощаем некоторые шаблоны кода
    # Это требует более сложного анализа и может быть реализовано позднее
    
    return code

def deobfuscate_layer11_improved(input_file, output_file):
    """
    Основная функция улучшенной деобфускации слоя 11
    """
    # Загружаем код из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Исходный размер файла: {original_size} байт")
    
    # Определяем список печатных символов
    global printable_chars
    printable_chars = set("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r")
    
    # Извлекаем ключ XOR
    print("Извлечение ключа XOR...")
    xor_key = extract_xor_key(code)
    if xor_key:
        print(f"Ключ XOR: {xor_key}")
    else:
        print("Не удалось извлечь ключ XOR")
    
    # Исправляем функцию xor_decode
    print("Исправление функции xor_decode...")
    code = fix_xor_decode_function(code)
    
    # Применяем функции деобфускации
    print("Декодирование всех строк...")
    code = decode_all_strings(code, xor_key)
    
    print("Исправление синтаксических ошибок...")
    code = fix_syntax_errors(code)
    
    print("Очистка вызовов decode('utf-8')...")
    code = clean_decode_calls(code)
    
    print("Упрощение вызовов getattr()...")
    code = simplify_getattr_calls(code)
    
    print("Очистка структуры импортов...")
    code = cleanup_imports(code)
    
    print("Проверка на наличие еще не декодированных строк...")
    code = extract_and_decode_strings(code, xor_key)
    
    print("Упрощение структур кода...")
    code = simplify_code_structures(code)
    
    # Сохраняем деобфусцированный код
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Новый размер файла: {new_size} байт")
    print(f"Разница: {new_size - original_size} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer11_improved("layer11.py", "layer12_improved.py") 