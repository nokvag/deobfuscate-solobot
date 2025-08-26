#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import ast
import json
from typing import ByteString, Union, Dict, List, Tuple, Set, Optional

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
        return f'"{("".join(parts))}"'
    
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

def detect_variable_roles(code: str) -> Dict[str, str]:
    """Анализирует код и определяет роли/назначение обфусцированных переменных"""
    var_roles = {}
    
    # Переменные, связанные с асинхронным вводом/выводом
    asyncio_pattern = r'(builtins\.asyncio|asyncio\.run|create_task|all_tasks|current_task|Event|get_event_loop|sleep)'
    asyncio_vars = set()
    
    for match in re.finditer(r'\b([a-zA-Z][a-zA-Z0-9_]{5,})\b', code):
        var_name = match.group(1)
        
        # Контекст переменной - 100 символов до и после
        context_start = max(0, match.start() - 100)
        context_end = min(len(code), match.end() + 100)
        context = code[context_start:context_end]
        
        # Определяем роль переменной
        if re.search(r'bot|telegram|tg_|send_message', context, re.IGNORECASE):
            var_roles[var_name] = 'bot'
        elif re.search(asyncio_pattern, context):
            var_roles[var_name] = 'asyncio'
        elif re.search(r'aiohttp|TCPSite|AppRunner|web\.Application|router|get|post', context):
            var_roles[var_name] = 'web_server'
        elif re.search(r'path\.join|path\.expanduser|path\.abspath|executable', context):
            var_roles[var_name] = 'file_system'
        elif re.search(r'print|log|error|warning|info|exception', context):
            var_roles[var_name] = 'logger'
        elif re.search(r'webhook|url', context):
            var_roles[var_name] = 'webhook'
    
    return var_roles

def rename_variables(code: str, mapping: Dict[str, str] = None) -> str:
    """Переименовывает обфусцированные переменные на более понятные имена"""
    # Если не передана карта переименований, пытаемся определить автоматически
    if mapping is None:
        var_roles = detect_variable_roles(code)
        mapping = {}
        
        role_counters = {'bot': 0, 'asyncio': 0, 'web_server': 0, 'file_system': 0, 'logger': 0, 'webhook': 0, 'other': 0}
        
        for var, role in var_roles.items():
            role_counters[role] = role_counters.get(role, 0) + 1
            mapping[var] = f"{role}_{role_counters[role]}"
    
    # Применяем переименования
    for old_name, new_name in mapping.items():
        # Используем границы слова, чтобы не заменять части других переменных
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def remove_debug_comments(code: str) -> str:
    """Удаляет комментарии отладки, добавленные при деобфускации"""
    pattern = r'\s*\/\*\s*(?:xor_transform|ошибка|error).*?\*\/'
    return re.sub(pattern, '', code)

def fix_utf8_imports(code: str) -> str:
    """Исправляет обфусцированные импорты с 'utf-8'"""
    # Заменяем __import__('utf-8') на соответствующие модули
    replacements = {
        "__import__('utf-8')": "importlib.import_module('utf-8')",
        "patches('utf-8'": "importlib.import_module('utf-8'",
        "patches('utf-8', 'utf-8'": "importlib.import_module('utf-8'",
        "importlib.import_module('utf-8')": "importlib.import_module('asyncio')",
        "__import__('utf-8'),": "asyncio,",
        # Дополнительные замены можно добавить по мере обнаружения паттернов
    }
    
    for old, new in replacements.items():
        code = code.replace(old, new)
    
    return code

def clean_f_strings(code: str) -> str:
    """Исправляет обфусцированные f-строки"""
    # Паттерн для поиска строк вида: print(f✅ Коман + chr(994655 - 993579) + а `solobot` у)
    pattern = r'f([^"\'].*?)(\s*\+\s*.*?\+\s*.*)'
    
    # Заменяем на нормальные f-строки
    code = re.sub(pattern, r'f"\1"', code)
    
    return code

def apply_manual_fixes(code: str) -> str:
    """Применяет некоторые ручные исправления, которые сложно автоматизировать"""
    # Определяем известные подстановки
    substitutions = [
        # Фиксим очевидные замены
        ("'utf-8'", "'asyncio'"),
        ("importlib.import_module('utf-8')", "importlib.import_module('asyncio')"),
        ("'utf8'", "'asyncio'"),
        
        # Фиксим странные операторы
        (").utf-8(", ").exists("),
        (".utf-8(", ".is_dir("),
        ("KTcuB6QKV8WZ.utf-8", "os.access"),
        
        # Известные обфусцированные переменные
        ("diyel4O5bMLs", "asyncio_mod"),
        ("GiFJytvAvueM", "bot"),
        ("_dIJgk7A3AIg", "dispatcher"),
        ("zcptFAL0yWNU", "logger"),
        ("lqCBDe1lOEOd", "app"),
        ("fq44kslIKKlh", "web"),
        ("CixZZL1caaDz", "asyncio_sleep"),
        
        # Другие исправления
        ("if __name__ == 'utf-8':", "if __name__ == '__main__':"),
        ("if __name__ == 'asyncio':", "if __name__ == '__main__':"),
    ]
    
    for old, new in substitutions:
        code = code.replace(old, new)
    
    return code

def replace_obfuscated_strings(code: str) -> str:
    """Заменяет все оставшиеся обфусцированные строки на их предполагаемые значения"""
    # Основные замены для обфусцированных строк
    str_replacements = {
        "'utf-8'": "'asyncio'",
        # Можно добавить другие замены по мере необходимости
    }
    
    for old, new in str_replacements.items():
        code = code.replace(old, new)
    
    return code

def add_descriptive_comments(code: str) -> str:
    """Добавляет поясняющие комментарии к основным компонентам кода"""
    # Разделяем код на строки для удобства
    lines = code.split('\n')
    
    # Основные секции, которые нужно прокомментировать
    sections = {
        "def QK5bLxBOypkF": "# Функция для установки команды solobot",
        "async def WeQFJHP3LH_W": "# Основная функция запуска бота",
        "async def D6P0eecBAFVv": "# Функция обработки сообщений",
        "async def M6flxKL4gRoX": "# Функция настройки вебхука",
        "async def KMS7j9IC8wK5": "# Функция завершения работы",
        "async def o_Zg3SYZ2U_F": "# Функция остановки веб-сервера",
    }
    
    # Добавляем комментарии
    result = []
    for line in lines:
        for pattern, comment in sections.items():
            if line.startswith(pattern):
                result.append(comment)
                break
        result.append(line)
    
    return '\n'.join(result)

def final_format_code(code: str) -> str:
    """Применяет финальное форматирование к коду"""
    # Удаляем лишние пустые строки
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    return code

def deobfuscate_file(input_file, output_prefix, max_passes=5, debug=False, rename_vars=True, add_comments=True):
    """Многопроходная деобфускация файла с улучшенными возможностями"""
    print(f"Начинаю улучшенную деобфускацию файла {input_file}...")
    
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
        
        # Шаг 8: Исправление импортов utf-8
        print("  Шаг 8: Исправление импортов utf-8...")
        code = fix_utf8_imports(code)
        
        # Шаг 9: Очистка f-строк
        print("  Шаг 9: Очистка f-строк...")
        code = clean_f_strings(code)
        
        # Шаг 10: Применение ручных исправлений
        print("  Шаг 10: Применение ручных исправлений...")
        code = apply_manual_fixes(code)
        
        # Сохраняем промежуточный результат
        step_file = os.path.join('deobfuscation_steps', f"{output_prefix}_pass{i+1}.py")
        with open(step_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"  Результат прохода {i+1} сохранен в {step_file}")
        
        # Проверяем, изменился ли код после этого прохода
        if code == previous_code:
            print(f"  Код не изменился после прохода {i+1}, завершаем деобфускацию")
            break
    
    # Финальная очистка и улучшения
    print("\nФинальная обработка кода...")
    
    # Удаляем комментарии отладки
    code = remove_debug_comments(code)
    
    # Очистка импортов
    code = cleanup_imports(code)
    
    # Замена оставшихся обфусцированных строк
    code = replace_obfuscated_strings(code)
    
    # Переименование переменных
    if rename_vars:
        print("  Переименование переменных...")
        code = rename_variables(code)
    
    # Добавление комментариев
    if add_comments:
        print("  Добавление поясняющих комментариев...")
        code = add_descriptive_comments(code)
    
    # Финальное форматирование
    code = final_format_code(code)
    
    # Сохраняем итоговый результат
    final_output = f"{output_prefix}_deobfuscated.py"
    with open(final_output, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\nДеобфускация завершена. Итоговый результат сохранен в {final_output}")
    print("""
Дополнительная информация:
1. Код был деобфусцирован, но может требовать ручной доработки
2. Переменные переименованы на основе их предполагаемых ролей
3. Добавлены поясняющие комментарии к основным компонентам
4. Для лучшей читаемости используйте форматер кода (black, autopep8)
""")

def main():
    if len(sys.argv) < 2:
        print("Использование: python final_decoder_improved.py <input_file> [output_prefix] [опции]")
        print("Опции:")
        print("  --debug            Включить отладочные сообщения и комментарии в коде")
        print("  --no-rename        Отключить переименование переменных")
        print("  --no-comments      Отключить добавление комментариев")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = next((arg for arg in sys.argv[2:] if not arg.startswith('--')), "layer10_final")
    
    debug_mode = "--debug" in sys.argv
    rename_vars = "--no-rename" not in sys.argv
    add_comments = "--no-comments" not in sys.argv
    
    deobfuscate_file(
        input_file, 
        output_prefix, 
        debug=debug_mode, 
        rename_vars=rename_vars, 
        add_comments=add_comments
    )

if __name__ == "__main__":
    main() 