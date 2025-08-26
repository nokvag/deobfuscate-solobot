#!/usr/bin/env python3

import re
import ast
import os

def xor_decode(data):
    """
    Декодирует данные, используя XOR-шифрование с ключом
    """
    # Ключ XOR (извлеченный из оригинальной функции)
    key = [
        52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
        103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
        76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
        58, 48, 248, 136, 234, 128, 174, 58, 109, 129
    ]
    
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def fix_function_definitions(code):
    """
    Исправляет определения функций в коде
    """
    # Исправляем определение функции xor_decode
    code = code.replace("def xor_decodedata:", "def xor_decode(data):")
    
    # Исправляем проблемы с enumerate и len
    code = code.replace("lenkey", "len(key)")
    code = code.replace("enumeratedata", "enumerate(data)")
    
    # Исправляем случаи, когда функции склеены
    code = code.replace("bytes([b ^ key[i % len(key)] for i, b in enumerate(data)]).def", 
                     "bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])\n\ndef")
    
    # Исправляем случаи, когда функции искажены иначе
    code = re.sub(r"bytes\(\[b \^ key\[i % len\(key\)\] for i, b in enumerate\(data\)\]\)\.def\(([\s\S]+?)\):",
                 r"bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])\n\ndef \1:", code)
    
    # Исправляем возвращаемое значение функции
    code = re.sub(r"return\s+bytes\(\[b \^ key\[i % len\(key\)\] for i, b in enumerate\(data\)\]\)\.def",
                 r"return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])\n\ndef", code)
    
    return code

def fix_try_except_blocks(code):
    """
    Исправляет блоки try-except
    """
    # Исправляем случаи, когда except присоединен к предыдущей строке
    code = code.replace(").except", ")\nexcept")
    
    # Исправляем отступы в блоке try-except
    pattern = r"try:\s*([^\n]+)\s*except\s+([^:]+):\s*([^\n]+)"
    replacement = r"try:\n    \1\nexcept \2:\n    \3"
    code = re.sub(pattern, replacement, code)
    
    return code

def fix_decode_calls(code):
    """
    Исправляет вызовы decode
    """
    # Исправляем неправильные вызовы decode
    code = re.sub(r"decode,\s*\)", r"decode()", code)
    code = re.sub(r"decode\s*\(\s*\)\s*\(\s*'utf-8'\s*\)", r"decode('utf-8')", code)
    
    # Исправляем случаи b'...'.decode
    pattern = r"(b'[^']*'|b\"[^\"]*\")(?:\.decode\s*$|\.decode\s+|\.decode(?!\())"
    code = re.sub(pattern, r"\1.decode('utf-8')", code)
    
    # Исправляем вызовы getattr с decode
    pattern = r"getattr\(([^,]+),\s*['\"]decode['\"]\s*(?:,\s*[^)]*\s*)?\)\s*\(\s*['\"]utf-8['\"]\s*\)"
    code = re.sub(pattern, r"\1.decode('utf-8')", code)
    
    # Исправляем случаи, когда decode неполный
    pattern = r"\.decode\s*\n"
    code = re.sub(pattern, r".decode('utf-8')\n", code)
    
    # Исправляем случаи, когда декодирование вложено в декодирование
    pattern = r"\.decode\(['\"]utf-8['\"]\)\.decode\(['\"]utf-8['\"]\)"
    code = re.sub(pattern, r".decode('utf-8')", code)
    
    # Исправляем случаи, когда b'...' без decode
    pattern = r"(b'[^']*'|b\"[^\"]*\")(?!\s*\.\s*decode)"
    code = re.sub(pattern, r"\1.decode('utf-8')", code)
    
    return code

def fix_string_formatting(code):
    """
    Исправляет форматирование строк
    """
    # Исправляем f-строки
    pattern = r"ff['\"]([^'\"]*)\{([^}]+)\}([^'\"]*)['\"]"
    code = re.sub(pattern, r"f'\1{\2}\3'", code)
    
    # Исправляем строки с "decode('utf-8')" внутри них
    pattern = r"['\"]([^'\"]*?)\.decode\(['\"]utf-8['\"]\)([^'\"]*?)['\"]"
    code = re.sub(pattern, r"'\1\2'", code)
    
    return code

def fix_getattr_calls(code):
    """
    Исправляет вызовы getattr
    """
    # Исправляем простые вызовы getattr
    pattern = r"getattr\(([^,]+),\s*['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"](?:\s*,\s*[^)]*\s*)?\)"
    
    def getattr_replacer(match):
        obj = match.group(1).strip()
        attr = match.group(2).strip()
        
        # Проверка, можно ли заменить на прямой доступ к атрибуту
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if all(c in valid_chars for c in attr):
            return f"{obj}.{attr}"
        return match.group(0)
    
    code = re.sub(pattern, getattr_replacer, code)
    
    return code

def fix_conditional_statements(code):
    """
    Исправляет условные операторы
    """
    # Исправляем if-else конструкции
    code = code.replace(".else", " else")
    code = code.replace(".if", " if")
    code = code.replace(".for", " for")
    code = code.replace(".while", " while")
    code = code.replace(".try", " try")
    code = code.replace(".finally", " finally")
    code = code.replace(".except", " except")
    code = code.replace(".with", " with")
    code = code.replace(".as", " as")
    code = code.replace(".return", " return")
    code = code.replace(".await", " await")
    code = code.replace(".async", " async")
    
    # Исправляем условия if-else без разделителей
    code = re.sub(r"(if\s+[^:]+)(?=else)", r"\1:", code)
    
    return code

def fix_xor_decode_patterns(code):
    """
    Заменяет закодированные строки их декодированными значениями
    """
    # Заменяем unknown_1 на xor_decode
    code = code.replace("unknown_1(", "xor_decode(")
    
    # Ищем все закодированные строки
    pattern = r"xor_decode\(\s*b['\"]([^'\"]*)['\"](?:\s*\.\s*decode\(['\"]utf-8['\"])?(?:\s*\))?\s*\)(?:\s*\.\s*decode(?:\(['\"]utf-8['\"])?)?"
    
    def decode_replacer(match):
        try:
            encoded = match.group(1)
            # Преобразуем экранированные последовательности в байты
            encoded_bytes = eval(f"b'{encoded}'")
            # Декодируем с помощью XOR
            decoded = xor_decode(encoded_bytes)
            # Пытаемся преобразовать в строку
            try:
                decoded_str = decoded.decode('utf-8')
                return f'"{decoded_str}"'
            except UnicodeDecodeError:
                # Если не удалось декодировать, оставляем как есть
                return match.group(0)
        except Exception:
            return match.group(0)
    
    return re.sub(pattern, decode_replacer, code)

def fix_parentheses(code):
    """
    Исправляет избыточные или неправильные скобки
    """
    # Удаляем конструкции вида " ).("
    code = re.sub(r"\s*\)\s*\.\s*\(\s*", ".", code)
    
    # Исправляем случаи, когда вызов метода неправильно записан
    code = re.sub(r"\)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", r").\1(", code)
    
    # Исправляем неправильные выражения с скобками
    code = re.sub(r"\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\.", r"(\1.", code)
    
    # Правильное расположение оператора точки в иерархии вызовов
    code = re.sub(r"\)\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)", r").\1", code)
    
    return code

def fix_chained_calls(code):
    """
    Исправляет цепочки вызовов
    """
    # Исправляем случаи, когда вызовы методов неправильно разделены
    code = re.sub(r"\)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?!\()", r").\1", code)
    
    # Исправляем случаи, когда нет точки между методами
    code = re.sub(r"([a-zA-Z_][a-zA-Z0-9_]*)\)([a-zA-Z_][a-zA-Z0-9_]*)", r"\1).\2", code)
    
    # Исправляем несогласованные скобки в вызовах методов
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*([^()]*?)\s*\)\s*([a-zA-Z_][a-zA-Z0-9_]*)"
    replacement = r"\1(\2).\3"
    code = re.sub(pattern, replacement, code)
    
    return code

def fix_imports(code):
    """
    Исправляет проблемы с импортами
    """
    # Заменяем странные импорты на нормальные
    code = re.sub(r"__import__\(\s*['\"]oh['\"]", r"__import__('os'", code)
    
    # Исправляем импорты с закодированными строками
    code = re.sub(r"__import__\(\s*b['\"][^'\"]+['\"]\.decode\(['\"]utf-8['\"]\)\s*\)", 
                 r"__import__('asyncio')", code)
    
    # Исправляем специальные строки
    code = re.sub(r"\[encoded\]['\"]\.decode", r"'asyncio'", code)
    
    # Исправляем импорты с hasattr
    pattern = r"if\s+hasattr\(import_module\(\s*['\"][^'\"]*['\"]\)\.else\("
    replacement = r"if hasattr(__import__('asyncio'), 'decode') else ("
    code = re.sub(pattern, replacement, code)
    
    return code

def fix_if_hasattr(code):
    """
    Исправляет конструкции if hasattr
    """
    # Исправляем неправильное форматирование if hasattr
    pattern = r"if\s+hasattr\(([^,]+),\s*['\"]([^'\"]+)['\"]\)(?:\.else\s*|\s+else\s+)\(\s*['\"]([^'\"]+)['\"](?:\s*\))?"
    replacement = r"if hasattr(\1, '\2') else '\3'"
    code = re.sub(pattern, replacement, code)
    
    return code

def insert_line_breaks(code):
    """
    Добавляет переносы строк для улучшения читаемости
    """
    # Добавляем перенос строки перед определенными ключевыми словами
    for keyword in ["def", "class", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "async"]:
        pattern = rf"([^\n])\s*{keyword}\s+"
        code = re.sub(pattern, rf"\1\n{keyword} ", code)
    
    return code

def fix_multiple_closing_parentheses(code):
    """
    Исправляет последовательные закрывающие скобки
    """
    # Добавляем перенос строки между последовательными закрывающими скобками
    pattern = r"\)\s*\)"
    replacement = r")\n)"
    code = re.sub(pattern, replacement, code)
    
    return code

def fix_embedded_function_calls(code):
    """
    Исправляет вложенные вызовы функций
    """
    # Преобразуем вызовы типа function1(function2(args)) в более читаемую форму
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\(\s*([^()]*?)\s*\)\s*\)"
    replacement = r"\1(\2(\3))"
    code = re.sub(pattern, replacement, code)
    
    return code

def clean_up_syntax(code):
    """
    Окончательная очистка синтаксиса
    """
    # Исправляем случаи, когда байтовая строка содержит .decode внутри
    pattern = r"b['\"]([^'\"]*?)\.decode\(['\"]utf-8['\"]\)([^'\"]*?)['\"]"
    replacement = r"b'\1\2'.decode('utf-8')"
    code = re.sub(pattern, replacement, code)
    
    # Удаляем двойные пробелы
    code = re.sub(r"\s{2,}", " ", code)
    
    # Исправляем отсутствующие двоеточия после условий
    code = re.sub(r"(if|while|for|def|class|with|try|except|finally)\s+([^:]+?)(?=\s*\n)", r"\1 \2:", code)
    
    # Исправляем неправильные двоеточия в середине выражений
    code = re.sub(r":\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", r".\1(", code)
    
    return code

def fix_missing_parentheses(code):
    """
    Добавляет отсутствующие закрывающие скобки
    """
    # Подсчитываем количество открывающих и закрывающих скобок
    open_count = code.count('(')
    close_count = code.count(')')
    
    # Добавляем недостающие закрывающие скобки в конец файла
    if open_count > close_count:
        code += ')' * (open_count - close_count)
    
    return code

def deobfuscate_code(input_file):
    """
    Основная функция деобфускации
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Шаг 1: Исправляем определения функций
    code = fix_function_definitions(code)
    
    # Шаг 2: Исправляем блоки try-except
    code = fix_try_except_blocks(code)
    
    # Шаг 3: Исправляем вызовы decode
    code = fix_decode_calls(code)
    
    # Шаг 4: Исправляем форматирование строк
    code = fix_string_formatting(code)
    
    # Шаг 5: Исправляем вызовы getattr
    code = fix_getattr_calls(code)
    
    # Шаг 6: Исправляем условные операторы
    code = fix_conditional_statements(code)
    
    # Шаг 7: Исправляем конструкции if hasattr
    code = fix_if_hasattr(code)
    
    # Шаг 8: Исправляем импорты
    code = fix_imports(code)
    
    # Шаг 9: Декодируем закодированные строки
    code = fix_xor_decode_patterns(code)
    
    # Шаг 10: Исправляем скобки
    code = fix_parentheses(code)
    
    # Шаг 11: Исправляем цепочки вызовов
    code = fix_chained_calls(code)
    
    # Шаг 12: Добавляем переносы строк
    code = insert_line_breaks(code)
    
    # Шаг 13: Исправляем последовательные закрывающие скобки
    code = fix_multiple_closing_parentheses(code)
    
    # Шаг 14: Исправляем вложенные вызовы функций
    code = fix_embedded_function_calls(code)
    
    # Шаг 15: Окончательная очистка синтаксиса
    code = clean_up_syntax(code)
    
    # Шаг 16: Исправляем отсутствующие закрывающие скобки
    code = fix_missing_parentheses(code)
    
    return code

def main():
    input_file = "layer13.py"
    output_file = "layer13_deobfuscated.py"
    
    # Деобфускация кода
    deobfuscated_code = deobfuscate_code(input_file)
    
    # Сохранение результата
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(deobfuscated_code)
    
    print(f"Файл {input_file} успешно деобфусцирован и сохранен как {output_file}")

if __name__ == "__main__":
    main() 