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

def fix_missing_returns(code: str) -> str:
    """Исправляет отсутствующие return операторы"""
    # Находим web_server_1, который, вероятно, должен быть return
    code = re.sub(r'\bweb_server_1\s+', 'return ', code)
    return code

def fix_syntax_errors(code: str) -> str:
    """Исправляет основные синтаксические ошибки в коде"""
    # Исправляем отсутствующие ключевые слова except
    code = re.sub(r'\bweb_server_29\s+web_server_30\s+as\s+web_server_31:', 'except Exception as web_server_31:', code)
    # Исправляем отсутствующие ключевые слова finally
    code = re.sub(r'\bweb_server_54:', 'finally:', code)
    return code

def fix_broken_function_calls(code: str) -> str:
    """Исправляет сломанные вызовы функций"""
    # Исправляем случаи, где строка заканчивается на .web_server_6( или похожие
    pattern = r'([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\((.*?)\)'
    
    def fix_call(match):
        obj = match.group(1)
        method = match.group(2)
        args = match.group(3)
        if method == 'web_server_6':
            method = 'decode'
        elif method == 'asyncio_6':
            method = 'is_dir'
        elif method == 'utf-8':
            method = 'exists'
        return f"{obj}.{method}({args})"
    
    return re.sub(pattern, fix_call, code)

def fix_syntax_quotes(code: str) -> str:
    """Исправляет проблемы с синтаксисом кавычек"""
    # Исправляем обрывающиеся строки без закрывающей кавычки
    pattern = r'([a-zA-Z0-9_]+)\.utf"-8\(([^)]+)\)'
    code = re.sub(pattern, r'\1.log(\2)', code)
    
    # Другие исправления с кавычками
    problematic_patterns = [
        (r'"d""\s*"([^"]+)"', r'"d" + "\1"'),  # "d""utf-8" -> "d" + "utf-8"
        (r'\bweb_server_6\("([^"]+)"\)', r'decode("\1")'),  # web_server_6("utf-8") -> decode("utf-8")
    ]
    for pattern, replacement in problematic_patterns:
        code = re.sub(pattern, replacement, code)
    
    return code

def detect_variable_roles(code: str) -> Dict[str, str]:
    """Анализирует код и определяет роли/назначение обфусцированных переменных"""
    var_roles = {}
    
    # Переменные, связанные с асинхронным вводом/выводом
    asyncio_pattern = r'(builtins\.asyncio|asyncio\.run|create_task|all_tasks|current_task|Event|get_event_loop|sleep)'
    
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

def prepare_variable_mapping() -> Dict[str, str]:
    """Подготавливает вручную проверенное отображение переменных"""
    # Ручное сопоставление для более точного переименования
    mapping = {
        # Основные функции и переменные
        "web_server_1": "return",
        "web_server_2": "asyncio",
        "web_server_3": "asyncio_mod",
        "web_server_4": "getattr",
        "web_server_5": "import_module",
        "web_server_6": "decode",
        "web_server_7": "globals",
        "web_server_8": "locals",
        "web_server_9": "host",
        "web_server_10": "port",
        "web_server_11": "use_post",
        "web_server_12": "use_get",
        "web_server_13": "vlARRACoCOHo",
        "web_server_14": "get_handler",
        "web_server_15": "check_token",
        "web_server_16": "post_handler",
        "web_server_17": "api_token",
        "web_server_18": "get_handler_impl",
        "web_server_19": "post_handler_impl",
        "web_server_20": "logger",
        "web_server_21": "task_impl",
        "web_server_22": "setup_solobot",
        "web_server_23": "script_path",
        "web_server_24": "os",
        "web_server_25": "python_path",
        "web_server_26": "folder",
        "web_server_27": "bot_path",
        "web_server_28": "file",
        "web_server_29": "except",
        "web_server_30": "Exception",
        "web_server_31": "err",
        "web_server_32": "interval",
        "web_server_33": "on_startup",
        "web_server_34": "on_shutdown",
        "web_server_35": "task",
        "web_server_36": "return_exceptions",
        "web_server_37": "stop_server",
        "web_server_38": "site",
        "web_server_39": "main",
        "web_server_40": "expected_token",
        "web_server_41": "use_webhook",
        "web_server_42": "tasks",
        "web_server_43": "Application",
        "web_server_44": "on_startup",
        "web_server_45": "on_shutdown",
        "web_server_46": "use_get_handler",
        "web_server_47": "use_post_handler",
        "web_server_48": "use_email_handler",
        "web_server_49": "runner",
        "web_server_50": "TCPSite",
        "web_server_51": "stop_event",
        "web_server_52": "loop",
        "web_server_53": "signal",
        "web_server_54": "finally",
        "web_server_55": "pending_tasks",
        
        # Bot-related
        "bot_1": "setup_webhook",
        "bot_2": "setup_webhook_routes",
        "bot_3": "sleep",
        "bot_4": "dispatcher",
        "bot_5": "webhook_path",
        "bot_6": "poll_timeout",
        "bot_7": "sleep_func",
        "bot_8": "handle_email_tg",
        "bot_9": "handle_email",
        "bot_10": "setup_webhook_impl",
        "bot_11": "solobot",
        "bot_12": "polling_task",
        "bot_13": "create_task",
        "bot_14": "router",
        "bot_15": "email_path_prefix",
        "bot_16": "AppRunner",
        
        # AsyncIO and file system
        "asyncio_1": "builtins",
        "asyncio_2": "ModuleType",
        "asyncio_3": "lambda",
        "asyncio_4": "signal_module",
        "asyncio_5": "webhook_url",
        "asyncio_6": "exists",
        "asyncio_7": "get_event_loop",
        "asyncio_8": "all_tasks",
        "asyncio_9": "current_task",
        
        "file_system_1": "importlib",
        "file_system_2": "import_module",
        "file_system_3": "abspath",
        "file_system_4": "sys",
        "file_system_5": "executable",
        "file_system_6": "paths",
        "file_system_7": "expanduser",
        "file_system_8": "X_OK"
    }
    
    return mapping

def rename_variables_with_mapping(code: str, mapping: Dict[str, str]) -> str:
    """Переименовывает переменные согласно предоставленному отображению"""
    for old_name, new_name in mapping.items():
        # Используем границы слова, чтобы не заменять части других переменных
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def replace_obfuscated_strings(code: str) -> str:
    """Заменяет все оставшиеся обфусцированные строки на их предполагаемые значения"""
    # Основные замены для обфусцированных строк
    str_replacements = {
        "'web_server_2'": "'asyncio'",
        "'utf-8'": "'asyncio'",
        '"web_server_2"': '"asyncio"',
        '"utf-8"': '"utf-8"',  # Оставляем как есть, если это действительно utf-8
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
        "def setup_solobot": "# Функция для установки команды solobot",
        "async def main": "# Основная функция запуска бота",
        "async def polling_task": "# Функция обработки сообщений в режиме polling",
        "async def on_startup": "# Функция настройки бота при запуске",
        "async def on_shutdown": "# Функция завершения работы бота",
        "async def stop_server": "# Функция остановки веб-сервера",
        "if __name__ == '__main__'": "# Точка входа в программу",
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

def fix_lambda_expressions(code: str) -> str:
    """Исправляет проблемы с лямбда-выражениями"""
    # Исправляем случаи вида 'asyncio_3 coro: None' на 'lambda coro: None'
    code = re.sub(r'(\w+)\s+(\w+):\s+None', r'lambda \2: None', code)
    return code

def final_format_code(code: str) -> str:
    """Применяет финальное форматирование к коду"""
    # Удаляем лишние пустые строки
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    # Исправляем отступы и форматирование
    lines = code.split('\n')
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def deobfuscate_file(input_file, output_prefix, max_passes=5, debug=False, rename_vars=True, add_comments=True):
    """Многопроходная деобфускация файла с улучшенными возможностями"""
    print(f"Начинаю углубленную деобфускацию файла {input_file}...")
    
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
        code = fix_syntax_quotes(code)
        
        # Шаг 8: Исправление лямбда-выражений
        print("  Шаг 8: Исправление лямбда-выражений...")
        code = fix_lambda_expressions(code)
        
        # Шаг 9: Исправление синтаксических ошибок
        print("  Шаг 9: Исправление синтаксических ошибок...")
        code = fix_syntax_errors(code)
        
        # Шаг 10: Исправление отсутствующих return
        print("  Шаг 10: Исправление отсутствующих return...")
        code = fix_missing_returns(code)
        
        # Шаг 11: Исправление сломанных вызовов функций
        print("  Шаг 11: Исправление сломанных вызовов функций...")
        code = fix_broken_function_calls(code)
        
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
    
    # Переименование переменных
    if rename_vars:
        print("  Переименование переменных с помощью заданного отображения...")
        mapping = prepare_variable_mapping()
        code = rename_variables_with_mapping(code, mapping)
    
    # Замена оставшихся обфусцированных строк
    print("  Замена оставшихся обфусцированных строк...")
    code = replace_obfuscated_strings(code)
    
    # Очистка импортов
    print("  Очистка импортов...")
    code = cleanup_imports(code)
    
    # Добавление комментариев
    if add_comments:
        print("  Добавление поясняющих комментариев...")
        code = add_descriptive_comments(code)
    
    # Финальное форматирование
    print("  Финальное форматирование кода...")
    code = final_format_code(code)
    
    # Сохраняем итоговый результат
    final_output = f"{output_prefix}_deobfuscated.py"
    with open(final_output, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"\nУглубленная деобфускация завершена. Итоговый результат сохранен в {final_output}")
    print("""
Дополнительная информация:
1. Исправлены основные синтаксические ошибки
2. Переменные переименованы на основе ручного сопоставления
3. Добавлены поясняющие комментарии к основным компонентам
4. Восстановлены отсутствующие ключевые слова (return, except и т.д.)
5. Для окончательной очистки кода рекомендуется использовать форматер (black, autopep8)
""")

def main():
    if len(sys.argv) < 2:
        print("Использование: python final_decoder_improved_v2.py <input_file> [output_prefix] [опции]")
        print("Опции:")
        print("  --debug            Включить отладочные сообщения и комментарии в коде")
        print("  --no-rename        Отключить переименование переменных")
        print("  --no-comments      Отключить добавление комментариев")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = next((arg for arg in sys.argv[2:] if not arg.startswith('--')), "layer10_final_improved")
    
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