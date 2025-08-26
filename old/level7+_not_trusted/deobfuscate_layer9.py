#!/usr/bin/env python3

import re
import ast
import os
import builtins
import keyword

def evaluate_string_concatenation(code):
    """
    Обрабатывает сложные конкатенации строк и упрощает их
    """
    # Ищем конкатенации строк вида "a" + "b" + "c"
    concat_pattern = r'("[^"\\]*(?:\\.[^"\\]*)*"\s*\+\s*)+("[^"\\]*(?:\\.[^"\\]*)*")'
    
    def replace_concat(match):
        # Извлекаем строку с конкатенацией
        concat_str = match.group(0)
        
        try:
            # Пытаемся вычислить строку с помощью eval
            result = eval(concat_str)
            
            # Возвращаем результат в виде одиночной строки
            return f'"{result}"'
        except:
            return concat_str
    
    # Заменяем конкатенации строк
    code = re.sub(concat_pattern, replace_concat, code)
    
    return code

def evaluate_hex_and_octal_strings(code):
    """
    Преобразует шестнадцатеричные и восьмеричные escape-последовательности в обычные строки
    """
    # Более простой и надежный подход
    def replace_escape_sequences(match):
        try:
            # Пробуем вычислить строку через ast.literal_eval
            return repr(ast.literal_eval(match.group(0)))
        except:
            # Если не удалось, просто возвращаем исходную строку
            return match.group(0)
    
    # Преобразуем строки, содержащие escape-последовательности
    string_pattern = r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
    code = re.sub(string_pattern, replace_escape_sequences, code)
    
    return code

def evaluate_ord_expressions(code):
    """
    Вычисляет выражения с ord() и заменяет их на числовые значения
    """
    ord_pattern = r'ord\(\s*(["\'][^"\']*["\'])\s*\)'
    
    def replace_ord(match):
        char = match.group(1)
        try:
            value = eval(f"ord({char})")
            return str(value)
        except:
            return match.group(0)
    
    code = re.sub(ord_pattern, replace_ord, code)
    
    return code

def simplify_byte_strings(code):
    """
    Упрощает сложные байтовые строки, включая строки с XOR-шифрованием
    """
    # Ищем байтовые литералы
    byte_pattern = r'b\'([^\']*)\'|b"([^"]*)"'
    
    def replace_byte_string(match):
        byte_str = match.group(0)
        
        try:
            # Пытаемся вычислить строку через eval
            result = eval(byte_str)
            
            # Если результат короткий, возвращаем его как есть
            if len(result) <= 10:
                return byte_str
            
            # Пытаемся декодировать как utf-8
            try:
                decoded = result.decode('utf-8')
                return f'"[Byte string: {decoded[:30]}...]"'
            except UnicodeDecodeError:
                return f'"[Binary data: {len(result)} bytes]"'
        except:
            return byte_str
    
    code = re.sub(byte_pattern, replace_byte_string, code)
    
    return code

def simplify_unknown_function(code):
    """
    Специальная обработка для функции unknown_1, которая выглядит как XOR-декодер
    """
    # Ищем определение функции unknown_1
    func_pattern = r'def unknown_1\(([^)]*)\):(.*?)(?=\ndef|\Z)'
    match = re.search(func_pattern, code, re.DOTALL)
    
    if match:
        func_body = match.group(2)
        
        # Проверяем, содержит ли функция операцию XOR с массивом
        if '^' in func_body and '[' in func_body and 'enumerate' in func_body:
            # Это вероятно XOR-декодер
            # Заменяем его на более понятную версию
            new_func = """def xor_decode(data):
    # Декодирует данные, используя XOR-шифрование с ключом
    # Ключ XOR (был извлечен из оригинальной функции)
    key = [
        52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
        103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
        76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
        58, 48, 248, 136, 234, 128, 174, 58, 109, 129
    ]
    
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])"""
            
            code = code.replace(match.group(0), new_func)
    
    return code

def simplify_int_expressions(code):
    """
    Вычисляет сложные выражения int() и заменяет их на числовые значения
    """
    # Ищем вызовы int() с восьмеричными числами через ord("\x08")
    int_pattern = r'int\(\s*([^,]+)(?:\s*,\s*ord\([\'"]\\x08[\'"]\))?\s*\)'
    
    def replace_int(match):
        expr = match.group(0)
        value_str = match.group(1)
        
        try:
            # Если есть восьмеричное число с ord("\x08"), вычисляем его
            if 'ord' in expr:
                # ord("\x08") == 8, что означает восьмеричную систему
                base = 8
                # Удаляем любые кавычки и + из строки
                clean_str = value_str.replace('"', '').replace("'", '').replace('+', '').replace(' ', '')
                # Заменяем 'o' и 'O' на '0' (часто используется для обфускации)
                clean_str = clean_str.replace('o', '0').replace('O', '0')
                
                try:
                    value = int(clean_str, base)
                    return str(value)
                except ValueError:
                    pass
            
            # Если простое выражение, пробуем вычислить
            value = eval(expr)
            return str(value)
        except:
            return expr
    
    code = re.sub(int_pattern, replace_int, code)
    
    return code

def simplify_getattr_calls(code):
    """
    Упрощает вызовы getattr() когда можно определить имя атрибута
    """
    # Ищем вызовы getattr с буквальными строками или сложными выражениями строк
    getattr_pattern = r'getattr\(\s*([^,]+)\s*,\s*([^,)]+)(?:\s*,\s*([^)]+))?\s*\)'
    
    def replace_getattr(match):
        obj = match.group(1)
        attr_expr = match.group(2)
        default = match.group(3)
        
        # Если атрибут - это простая строка
        if attr_expr.startswith('"') or attr_expr.startswith("'"):
            try:
                attr = eval(attr_expr)
                if default:
                    return f"{obj}.{attr} if hasattr({obj}, '{attr}') else {default}"
                else:
                    return f"{obj}.{attr}"
            except:
                pass
        
        # Если атрибут - конкатенация строк
        elif '+' in attr_expr and ('"' in attr_expr or "'" in attr_expr):
            try:
                attr = eval(attr_expr)
                if isinstance(attr, str):
                    if default:
                        return f"{obj}.{attr} if hasattr({obj}, '{attr}') else {default}"
                    else:
                        return f"{obj}.{attr}"
            except:
                pass
        
        # Если это декодирование байтовой строки
        elif 'decode' in attr_expr and ('utf-8' in attr_expr or 'utf8' in attr_expr):
            try:
                return f"{obj}.decode('utf-8')"
            except:
                pass
        
        # В остальных случаях оставляем как есть
        if default:
            return f"getattr({obj}, {attr_expr}, {default})"
        else:
            return f"getattr({obj}, {attr_expr})"
    
    code = re.sub(getattr_pattern, replace_getattr, code)
    
    return code

def replace_remaining_obfuscated_names(code):
    """
    Заменяет оставшиеся обфусцированные имена на более информативные
    """
    # Словарь типичных шаблонов имен для обфусцированных переменных
    name_patterns = {
        r'\bobfuscated_var_\d+\b': 'var_{}'
    }
    
    for pattern, template in name_patterns.items():
        matches = re.findall(pattern, code)
        unique_vars = {}
        
        for var in matches:
            if var not in unique_vars:
                # Присваиваем новое имя
                unique_vars[var] = template.format(len(unique_vars) + 1)
        
        # Заменяем имена
        for old_name, new_name in unique_vars.items():
            code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def remove_redundant_byteslike_strings(code):
    """
    Удаляет или заменяет сложные байтовые строки, которые не могут быть декодированы
    """
    # Заменяем фрагменты вида getattr(b'...', "decode") на более читаемый формат
    byteslike_pattern = r'getattr\(\s*b\'([^\']*)\'\s*,\s*["\']decode["\']'
    
    code = re.sub(byteslike_pattern, 'b"[encoded]".decode', code)
    
    return code

def cleanup_code(code):
    """
    Выполняет финальную чистку кода
    """
    # Удаляем избыточные пустые строки
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    # Удаляем избыточные комментарии
    code = re.sub(r'#\s*obfuscated.*$', '', code, flags=re.MULTILINE)
    
    return code

def deobfuscate_layer9(input_file, output_file):
    """
    Основная функция деобфускации слоя 9
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Размер исходного файла: {original_size} байт")
    
    # Последовательно применяем преобразования
    print("Обработка сложных строковых конкатенаций...")
    code = evaluate_string_concatenation(code)
    
    print("Обработка шестнадцатеричных и восьмеричных escape-последовательностей...")
    code = evaluate_hex_and_octal_strings(code)
    
    print("Вычисление выражений с ord()...")
    code = evaluate_ord_expressions(code)
    
    print("Упрощение функции unknown_1 (XOR-декодер)...")
    code = simplify_unknown_function(code)
    
    print("Упрощение сложных выражений int()...")
    code = simplify_int_expressions(code)
    
    print("Упрощение вызовов getattr()...")
    code = simplify_getattr_calls(code)
    
    print("Упрощение байтовых строк...")
    code = simplify_byte_strings(code)
    
    print("Удаление избыточных байтовых строк...")
    code = remove_redundant_byteslike_strings(code)
    
    print("Замена оставшихся обфусцированных имен...")
    code = replace_remaining_obfuscated_names(code)
    
    print("Финальная очистка кода...")
    code = cleanup_code(code)
    
    # Записываем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Размер деобфусцированного файла: {new_size} байт")
    print(f"Разница: {new_size - original_size} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer9("layer9.py", "layer10.py") 