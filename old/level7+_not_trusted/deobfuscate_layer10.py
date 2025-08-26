#!/usr/bin/env python3

import re
import ast
import os
import builtins
import keyword

def decode_bytes_literals(code):
    """
    Декодирует байтовые литералы в строки и заменяет их на строковые эквиваленты
    """
    # Ищем все байтовые литералы
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    
    def bytes_replacer(match):
        try:
            # Пробуем декодировать байты
            bytes_content = match.group(0)
            # Заменяем проблемные не-ASCII символы на их hex эквиваленты
            cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', bytes_content)
            
            # Пробуем вычислить значение
            try:
                value = eval(cleaned_bytes)
                if isinstance(value, bytes):
                    try:
                        # Пробуем декодировать байты как utf-8
                        decoded = value.decode('utf-8')
                        return f'"{decoded}"'
                    except UnicodeDecodeError:
                        # Если не удалось декодировать, возвращаем оригинальную, но очищенную строку
                        return cleaned_bytes
                else:
                    return cleaned_bytes
            except Exception as e:
                # Если не удалось вычислить значение, возвращаем оригинальную, но очищенную строку
                return cleaned_bytes
        except Exception as e:
            # В случае ошибки возвращаем оригинальную строку
            return match.group(0)
    
    # Заменяем все байтовые литералы
    code = re.sub(bytes_pattern, bytes_replacer, code)
    
    return code

def simplify_string_concatenations(code):
    """
    Упрощает строковые конкатенации типа 'a' + 'b' + 'c' до 'abc'
    """
    # Ищем последовательности строковых конкатенаций
    concat_pattern = r'([\'"][^\'"]*[\'"])\s*\+\s*([\'"][^\'"]*[\'"])'
    
    # Продолжаем поиск и замену, пока есть совпадения
    while re.search(concat_pattern, code):
        def concat_replacer(match):
            try:
                # Пробуем вычислить конкатенированную строку
                str1 = match.group(1)
                str2 = match.group(2)
                result = eval(f"{str1} + {str2}")
                return f'"{result}"'
            except Exception as e:
                # В случае ошибки возвращаем оригинальную строку
                return f"{match.group(1)} + {match.group(2)}"
        
        code = re.sub(concat_pattern, concat_replacer, code)
    
    return code

def simplify_getattr_calls(code):
    """
    Упрощает вызовы getattr() на прямой доступ к атрибутам
    """
    # Ищем вызовы getattr с двумя аргументами (объект и имя атрибута в виде строки)
    getattr_pattern = r'getattr\(([^,]+),\s*([\'"][^\'"]*[\'"])\s*\)'
    
    def getattr_replacer(match):
        try:
            obj = match.group(1).strip()
            attr = eval(match.group(2))
            return f"{obj}.{attr}"
        except Exception as e:
            # В случае ошибки возвращаем оригинальную строку
            return match.group(0)
    
    # Заменяем простые вызовы getattr
    code = re.sub(getattr_pattern, getattr_replacer, code)
    
    # Более сложные случаи с getattr, когда атрибут вычисляется из нескольких строк
    complex_getattr_pattern = r'getattr\(([^,]+),\s*([^,\)]+)\s*\)'
    
    def complex_getattr_replacer(match):
        try:
            obj = match.group(1).strip()
            attr_expr = match.group(2).strip()
            
            # Если выражение для атрибута выглядит как строка или конкатенация строк
            if (attr_expr.startswith("'") and attr_expr.endswith("'")) or \
               (attr_expr.startswith('"') and attr_expr.endswith('"')) or \
               ('+' in attr_expr and "'" in attr_expr or '"' in attr_expr):
                try:
                    attr = eval(attr_expr)
                    if isinstance(attr, str):
                        return f"{obj}.{attr}"
                except:
                    pass
            
            # Если не удалось упростить, возвращаем исходный код
            return match.group(0)
        except Exception as e:
            # В случае ошибки возвращаем оригинальную строку
            return match.group(0)
    
    # Пробуем упростить более сложные вызовы getattr
    code = re.sub(complex_getattr_pattern, complex_getattr_replacer, code)
    
    return code

def decode_xor_strings(code):
    """
    Находит вызовы xor_decode и пытается декодировать строки
    """
    # Ищем все вызовы xor_decode
    xor_decode_pattern = r'xor_decode\(b[\'"]([^\'"]*)[\'"](?:\s*\))?'
    
    # Получаем определение функции xor_decode для возможности ее прямого выполнения
    xor_decode_func_pattern = r'def xor_decode\(data\):(.*?)(?=def|\Z)'
    xor_decode_func_match = re.search(xor_decode_func_pattern, code, re.DOTALL)
    
    if xor_decode_func_match:
        xor_decode_func_body = xor_decode_func_match.group(1).strip()
        
        # Извлекаем ключ XOR из функции
        xor_key_pattern = r'key = \[([\d, \n]+)\]'
        xor_key_match = re.search(xor_key_pattern, xor_decode_func_body, re.DOTALL)
        
        if xor_key_match:
            # Преобразуем строку с ключом в список чисел
            key_str = xor_key_match.group(1).replace('\n', '').replace(' ', '')
            try:
                xor_key = eval(f"[{key_str}]")
                
                # Определяем функцию xor_decode для использования
                def xor_decode(data):
                    return bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(data)])
                
                # Заменяем вызовы xor_decode на декодированные строки
                def xor_decode_replacer(match):
                    try:
                        # Получаем байтовую строку и преобразуем ее в байты
                        byte_str = match.group(1)
                        # Заменяем проблемные не-ASCII символы на их hex эквиваленты
                        cleaned_bytes = re.sub(r'[^\x00-\x7F]', lambda m: f'\\x{ord(m.group(0)):02x}', byte_str)
                        byte_data = eval(f"b'{cleaned_bytes}'")
                        
                        # Применяем xor_decode
                        decoded_bytes = xor_decode(byte_data)
                        
                        # Пробуем преобразовать результат в строку
                        try:
                            decoded_str = decoded_bytes.decode('utf-8')
                            return f'"{decoded_str}"'
                        except UnicodeDecodeError:
                            # Если не удалось декодировать, возвращаем оригинальный вызов
                            return match.group(0)
                    except Exception as e:
                        # В случае ошибки возвращаем оригинальный вызов
                        return match.group(0)
                
                # Заменяем вызовы xor_decode
                code = re.sub(xor_decode_pattern, xor_decode_replacer, code)
            except Exception as e:
                print(f"Ошибка при извлечении ключа XOR: {e}")
    
    return code

def rename_variables(code):
    """
    Переименовывает переменные типа var_X на более осмысленные имена на основе их использования
    """
    # Словарь для хранения соответствия между именами переменных и их назначением
    var_meanings = {}
    
    # Ищем использование переменных в контексте модулей и библиотек
    module_patterns = {
        r'var_(\d+)\.path': 'os',
        r'var_(\d+)\.TCPSite': 'aiohttp',
        r'var_(\d+)\.AppRunner': 'aiohttp',
        r'var_(\d+)\.Event': 'asyncio',
        r'var_(\d+)\.all_tasks': 'asyncio',
        r'var_(\d+)\.run': 'asyncio'
    }
    
    for pattern, meaning in module_patterns.items():
        matches = re.findall(pattern, code)
        for var_id in matches:
            var_meanings[f'var_{var_id}'] = meaning
    
    # Ищем использование переменных в контексте бота и веб-сервера
    context_patterns = {
        r'var_(\d+)\.router': 'app',
        r'var_(\d+)\.decode': 'decode_func',
        r'await var_(\d+)\(\)': 'scheduler_task',
        r'var_(\d+)\.bot': 'dispatcher'
    }
    
    for pattern, meaning in context_patterns.items():
        matches = re.findall(pattern, code)
        for var_id in matches:
            var_meanings[f'var_{var_id}'] = meaning
    
    # Создаем словарь замен
    replacements = {}
    for var_name, meaning in var_meanings.items():
        # Счетчики для каждого типа значения
        if meaning not in replacements:
            replacements[meaning] = 0
        
        replacements[meaning] += 1
        
        # Создаем новое имя
        if replacements[meaning] == 1:
            new_name = meaning
        else:
            new_name = f"{meaning}_{replacements[meaning]}"
        
        # Заменяем переменную во всем коде
        code = re.sub(r'\b' + re.escape(var_name) + r'\b', new_name, code)
    
    # Для оставшихся var_X оставляем как есть или даем более общие имена
    # Это можно доработать для лучшего переименования, если необходимо
    
    return code

def simplify_conditional_logic(code):
    """
    Переименовывает функции conditional_logic_X на более осмысленные имена
    """
    # Словарь для хранения соответствия между именами функций и их назначением
    func_meanings = {
        'conditional_logic_1': 'import_module',
        'conditional_logic_2': 'install_solobot',
        'conditional_logic_3': 'periodic_task',
        'conditional_logic_4': 'on_startup',
        'conditional_logic_5': 'on_shutdown',
        'conditional_logic_6': 'handle_stop',
        'conditional_logic_7': 'main'
    }
    
    # Заменяем имена функций
    for old_name, new_name in func_meanings.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def cleanup_code(code):
    """
    Выполняет окончательную очистку кода
    """
    # Удаляем повторяющиеся пустые строки
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    # Заменяем сложные выражения для строк UTF-8
    code = re.sub(
        r"'u'\s*\+\s*'t'\s*\+\s*'f'\s*\+\s*'-'\s*\+\s*'8'",
        "'utf-8'",
        code
    )
    
    # Убираем неиспользуемые переменные
    # Это требует более сложного анализа, но можно реализовать в будущем
    
    return code

def deobfuscate_layer10(input_file, output_file):
    """
    Основная функция деобфускации слоя 10
    """
    # Загружаем код из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Исходный размер файла: {original_size} байт")
    
    # Применяем функции деобфускации
    print("Декодирование байтовых литералов...")
    code = decode_bytes_literals(code)
    
    print("Декодирование строк, зашифрованных с помощью XOR...")
    code = decode_xor_strings(code)
    
    print("Упрощение строковых конкатенаций...")
    code = simplify_string_concatenations(code)
    
    print("Упрощение вызовов getattr()...")
    code = simplify_getattr_calls(code)
    
    print("Переименование функций условной логики...")
    code = simplify_conditional_logic(code)
    
    print("Переименование переменных на основе их использования...")
    code = rename_variables(code)
    
    print("Окончательная очистка кода...")
    code = cleanup_code(code)
    
    # Сохраняем деобфусцированный код
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Новый размер файла: {new_size} байт")
    print(f"Разница: {new_size - original_size} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer10("layer10.py", "layer11.py") 