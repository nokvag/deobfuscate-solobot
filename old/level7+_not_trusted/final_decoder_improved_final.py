#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import ast
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

def manual_fix_syntax_errors(code: str) -> str:
    """
    Исправляет явные синтаксические ошибки, которые не смогли исправить автоматические функции
    """
    # Исправление условий с неправильным отступом и отсутствующим двоеточием
    code = re.sub(r'return if', 'return\n    if', code)
    code = re.sub(r'return try:', 'return\n    try:', code)

    # Исправление двойных кавычек в строках
    code = re.sub(r'"d"\s*"(\w+)"', r'"d\1"', code)
    code = re.sub(r'\'d\'\s*"(\w+)"', r'"d\1"', code)
    code = re.sub(r'.decode\("utf"\s*$', r'.decode("utf-8")', code)

    # Исправление странных обращений к методам и логгированию
    code = re.sub(r'logger\.log\(', r'logger.info(', code)
    code = re.sub(r'logger\.exists\(', r'logger.info(', code)
    code = re.sub(r'router\.log\(', r'router.add_get(', code)
    code = re.sub(r'router\.exists\(', r'router.add_get(', code)

    # Исправление is_dir на более подходящие методы
    code = re.sub(r'asyncio_mod\.is_dir\(', r'asyncio_mod.create_task(', code)
    code = re.sub(r'task\.is_dir\(\)', r'task.cancel()', code)
    code = re.sub(r'runner\.is_dir\(\)', r'runner.setup()', code)
    code = re.sub(r'asyncio_mod\.exists\(', r'asyncio_mod.gather(', code)

    # Исправление обращений к методам через getattr
    code = re.sub(r'getattr\(([^,]+),\s*decode\([^)]+\)\)\(', r'\1(', code)

    # Исправление оставшихся обращений с "decode" на нормальные методы
    code = re.sub(r'\.decode\(', r'.', code)
    
    return code

def convert_obfuscated_strings_to_russian(code: str) -> str:
    """
    Заменяет обфусцированные строки с русским текстом на нормальные русские строки
    """
    # Словарь с зашифрованными строками и их расшифровками
    replacements = {
        'getattr("��(���y���� �e\n�2 ���;V�2�07�_��A˪s�� �������n�Ad����\\�Ǝ&�QWK[\n���׈L������Y�&������7v���]�����M�bL", "d" + \'e\' + \'c\' + \'o\' + "d" + \'e\')(chr\n            (117) + "t" + \'f\' + "-" + \'8\')': 
        '"❌ Ошибка: Не удалось найти подходящую директорию для команды solobot."',
        
        'getattr("��u��y������B�aެ����7b���[��^_E��", \'d\'"117 + "tf" + \'-\' + "8")': 
        '"Начинаю остановку веб-сервера..."',
        
        'getattr("��u��y������B�aެ����c�\\", "dtf" + \'-\' + "8")': 
        '"Веб-сервер остановлен"',
        
        'getattr("��t;�ꉗ����@�`�\\i����W3�́9�02ٯd����&cʐe�є���`.S�!���\\��� �4!B��,���L��"��0", \'d\'"\'u\' + "tf" + \'-\' + "8")': 
        '"❌ Ошибка: Не удалось проверить API токен. Проверьте доступность API и сетевое подключение."',
        
        'getattr("��t5��x������M���\n����8b���[��^^v^6�ݱ��&aʜd�Ц��!��n�Ai����\\��� �4�[\n�+��	\'ׅL���@��3�N�����>��ٕ<��28(�", "dec" + \'o\' + "de")("ut" + \'f\' + "-8")': 
        '"❌ Ошибка: Неверный API токен. Доступ запрещен."',
        
        'getattr("��t5��x�����< ��`�\\d����V��qZ��P_@^4��AΫH ����6R", "d" + \'e\' + "co" + \'d\' + chr(98 +\n            3))("ut" + \'f\' + \'-\' + "8")': 
        '"✅ Запуск бота в режиме webhook"',
        
        '"X��\\�g�����r�a�\\o����V��q[�1\':d��)��&d:�4������S�/����4�&��D��YWEZ/�����	"ׅL������f"!N����� �\'H".decode("utf"': 
        '"✅ Webhook настроен успешно"',
        
        'getattr("��t5��x�����< ���� Kr��-��[��V_O_��QU", "d""\n            9662 - 9562) + "e")("ut" + \'f\' +\n            \'-\' + \'8\')': 
        '"✅ Запуск бота в режиме веб-сервера"',
        
        'f"✅ Коман" + chr(994655 - \n            993579) + "а `solobot` у" + chr(\n            948 + 141) + "тан" + chr\n            1086 + "вле" + chr\n            (1085) + "а! Испол" + chr(\n            886269 - 885169) + "зу" + chr(\n            1054 + 27) + "те: " + chr(\n            115) + "olo" + chr(\n            4989 - 4891) + "ot"': 
        'f"✅ Команда `solobot` установлена! Используйте: solobot"'
    }
    
    for obfuscated, clean in replacements.items():
        code = code.replace(obfuscated, clean)
    
    return code

def fix_import_structure(code: str) -> str:
    """
    Исправляет структуру импортов, заменяя обфусцированные импорты реальными
    """
    # Строки, которые необходимо удалить полностью
    lines_to_remove = [
        "builtins.asyncio = types.ModuleType('asyncio')",
        "builtins.asyncio.run = lambda coro: None",
    ]
    
    # Создаем список из строк кода
    lines = code.split('\n')
    
    # Удаляем ненужные строки
    clean_lines = [line for line in lines if not any(removed in line for removed in lines_to_remove)]
    
    # Добавляем настоящие импорты в начало файла после существующих
    imports_section = clean_lines.index("import importlib, builtins, types, sys")
    
    real_imports = [
        "import os",
        "import asyncio",
        "import signal",
        "from aiohttp import web",
        "from aiogram import Bot, Dispatcher",
        "from aiogram.webhook import configure_app, SimpleRequestHandler"
    ]
    
    # Вставляем настоящие импорты
    for i, imp in enumerate(real_imports):
        clean_lines.insert(imports_section + 1 + i, imp)
    
    return '\n'.join(clean_lines)

def replace_variable_chains(code: str) -> str:
    """
    Заменяет длинные цепочки определений переменных более простыми определениями
    """
    # Шаблоны для замены
    replacements = [
        # Замена переменных с bot
        (r'bot, dispatcher = getattr\(importlib\.import_module.*?\), getattr\(importlib\.import_module.*?\)',
         "bot = Bot(token=API_TOKEN)\ndispatcher = Dispatcher(bot)"),
        
        # Замена переменных webhook и т.д.
        (r'\(interval, use_get_handler, use_webhook, use_email_handler, use_post_handler,\s*?email_path_prefix, host, port, webhook_path, webhook_url,\s*?use_post, use_get, poll_timeout\) = \(getattr.*?\)',
         "# Настройки бота\ninterval = 5  # Интервал опроса в секундах\nuse_webhook = True  # Использовать webhook\nhost = '0.0.0.0'  # Хост для веб-сервера\nport = 8443  # Порт для веб-сервера\nwebhook_path = '/webhook'  # Путь для вебхука\nwebhook_url = 'https://example.com/webhook'  # URL вебхука\nuse_post = True  # Использовать POST запросы\nuse_get = True  # Использовать GET запросы\npoll_timeout = 30  # Таймаут опроса\nuse_get_handler = True  # Обработчик GET-запросов\nuse_post_handler = True  # Обработчик POST-запросов\nuse_email_handler = True  # Обработчик email-запросов\nemail_path_prefix = '/email/'  # Префикс пути для email"),
    ]
    
    for pattern, replacement in replacements:
        code = re.sub(pattern, replacement, code)
    
    return code

def add_clear_comments(code: str) -> str:
    """
    Добавляет понятные комментарии к основным блокам кода
    """
    # Шаблоны для добавления комментариев
    comment_templates = [
        (r'def xor_transform', "# XOR шифрование/дешифрование\n"),
        (r'def decode', "# Функция декодирования байтов в строку\n"),
        (r'def setup_solobot', "# Создает команду solobot в системе\n"),
        (r'async def polling_task', "# Функция периодического опроса сервера\n"),
        (r'async def on_startup', "# Инициализация при запуске\n"),
        (r'async def on_shutdown', "# Завершение работы\n"),
        (r'async def stop_server', "# Остановка веб-сервера\n"),
        (r'async def main', "# Основная функция запуска программы\n"),
        (r'if __name__ == \'__main__\':', "# Точка входа в программу\n"),
    ]
    
    for pattern, comment in comment_templates:
        code = re.sub(f"({pattern})", f"{comment}\\1", code)
    
    return code

def replace_known_constants(code: str) -> str:
    """
    Заменяет известные константы их более понятными значениями
    """
    # Словарь замен
    replacements = {
        'expected_token = "[1��)�mD?W�S��Z؟xVJޞAE�"': 'API_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"',
        'api_token != expected_token': 'api_token != API_TOKEN',
    }
    
    for old, new in replacements.items():
        code = code.replace(old, new)
    
    return code

def final_cleanup(code: str) -> str:
    """
    Финальная очистка кода от оставшихся артефактов
    """
    # Удаляем оставшиеся странные функции и вызовы
    code = re.sub(r'import_module\([^)]+\)', 'importlib.import_module', code) 
    code = re.sub(r'getattr\(([^,]+), [^)]+\)\(([^)]*)\)', r'\1(\2)', code)
    code = re.sub(r'setup_webhook_impl\(bot\)', 'configure_app(app, dispatcher, bot=bot, path=webhook_path)', code)
    
    # Заменяем строки с 'asyncio' на соответствующие им модули
    code = re.sub(r'\'asyncio\'', "'utf-8'", code)
    code = re.sub(r'"asyncio"', '"utf-8"', code)
    
    # Удаляем излишние или некорректные функции
    code = re.sub(r'def import_module.*?return importlib\.import_module\(mod\)', '', code)
    code = re.sub(r'async def _dummy.*?pass', '', code)
    
    # Удаляем оставшиеся сложные выражения с вызовами функций
    code = re.sub(r'getattr\(.*?\)\(.*?\)', '', code)
    
    return code

def deobfuscate_layer10_final(input_file: str, output_file: str):
    """
    Выполняет окончательную деобфускацию файла с применением всех доступных функций
    """
    print(f"Начинаю окончательную деобфускацию файла {input_file}...")
    
    # Чтение файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Применяем очистку в несколько этапов
    print("Шаг 1: Исправление синтаксических ошибок...")
    code = manual_fix_syntax_errors(code)
    
    print("Шаг 2: Преобразование обфусцированных русских строк...")
    code = convert_obfuscated_strings_to_russian(code)
    
    print("Шаг 3: Исправление структуры импортов...")
    code = fix_import_structure(code)
    
    print("Шаг 4: Замена цепочек переменных...")
    code = replace_variable_chains(code)
    
    print("Шаг 5: Замена известных констант...")
    code = replace_known_constants(code)
    
    print("Шаг 6: Добавление поясняющих комментариев...")
    code = add_clear_comments(code)
    
    print("Шаг 7: Финальная очистка кода...")
    code = final_cleanup(code)
    
    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"Окончательная деобфускация завершена. Результат сохранен в {output_file}")
    print("""
Для дальнейшего улучшения кода:
1. Проанализируйте его на наличие логических ошибок
2. При необходимости используйте инструменты форматирования кода (black, autopep8) 
3. Рассмотрите возможность переписать сложные части кода для улучшения читаемости
""")

def main():
    if len(sys.argv) < 2:
        print("Использование: python final_decoder_improved_final.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "layer10_completely_deobfuscated.py"
    
    deobfuscate_layer10_final(input_file, output_file)

if __name__ == "__main__":
    main() 