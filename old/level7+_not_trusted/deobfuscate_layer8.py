#!/usr/bin/env python3

import re
import ast
import os
import builtins
import keyword

def analyze_tuple_structure(code):
    """
    Анализирует структуру начального кортежа в файле
    Обычно этот кортеж содержит перезаписанные встроенные функции и типы Python
    """
    # Ищем открывающую и закрывающую скобки кортежа
    tuple_start = code.find('(')
    if tuple_start == -1:
        return None, None
    
    # Ищем закрывающую скобку с учетом вложенности
    depth = 1
    tuple_end = tuple_start + 1
    while depth > 0 and tuple_end < len(code):
        if code[tuple_end] == '(':
            depth += 1
        elif code[tuple_end] == ')':
            depth -= 1
        tuple_end += 1
    
    if depth != 0:
        return None, None
    
    # Извлекаем содержимое кортежа
    tuple_content = code[tuple_start:tuple_end]
    
    # Ищем присваивание этому кортежу
    assignment_match = re.search(r'\)\s*=\s*\(', code[tuple_end:])
    if not assignment_match:
        return tuple_content, None
    
    # Ищем конец второго кортежа (значения)
    values_start = tuple_end + assignment_match.end()
    depth = 1
    values_end = values_start
    while depth > 0 and values_end < len(code):
        if code[values_end] == '(':
            depth += 1
        elif code[values_end] == ')':
            depth -= 1
        values_end += 1
    
    if depth != 0:
        return tuple_content, None
    
    values_content = code[values_start-1:values_end]
    
    return tuple_content, values_content

def get_builtin_functions_and_types():
    """
    Возвращает список встроенных функций и типов Python
    """
    # Собираем все встроенные функции и типы, сортируя их по наиболее часто используемым
    common_builtins = [
        'print', 'int', 'str', 'list', 'dict', 'tuple', 'set',
        'len', 'range', 'open', 'isinstance', 'type', 'bytes',
        'bool', 'float', 'sum', 'max', 'min', 'sorted', 'enumerate',
        'zip', 'map', 'filter', 'any', 'all', 'chr', 'ord', 'eval',
        'exec', 'compile', 'getattr', 'setattr', 'hasattr', 'dir',
        'globals', 'locals', 'id', 'hash', 'repr', 'format', 'input'
    ]
    
    # Добавляем исключения
    exceptions = [
        'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
        'ImportError', 'NameError', 'SyntaxError', 'AttributeError',
        'FileNotFoundError', 'OSError', 'RuntimeError', 'StopIteration'
    ]
    
    # Добавляем остальные встроенные имена
    other_builtins = [name for name in dir(builtins) 
                      if not name.startswith('_') and 
                      name not in common_builtins and 
                      name not in exceptions]
    
    # Собираем всё вместе в порядке предполагаемой частоты использования
    all_builtins = common_builtins + exceptions + other_builtins
    
    # Добавляем ключевые слова Python
    python_keywords = list(keyword.kwlist)
    
    return all_builtins, python_keywords

def extract_builtin_mapping(tuple_content):
    """
    Извлекает соответствие обфусцированных имен встроенным функциям
    """
    # Извлекаем все имена переменных из кортежа
    var_pattern = r'obfuscated_var_\d+'
    var_names = re.findall(var_pattern, tuple_content)
    
    # Получаем список встроенных функций и типов
    builtins_list, _ = get_builtin_functions_and_types()
    
    # Сопоставляем переменные и встроенные имена
    mapping = {}
    for i, var_name in enumerate(var_names):
        if i < len(builtins_list):
            mapping[var_name] = builtins_list[i]
    
    return mapping

def scan_for_normal_names(code):
    """
    Ищет нормальные имена Python в коде, которые указывают на реальное значение обфусцированных переменных
    """
    normal_names = {}
    
    # Словарь паттернов для распознавания функций по их использованию
    function_patterns = {
        'print': [
            # print с одним строковым аргументом
            r'(obfuscated_var_\d+)\s*\(\s*[\'"]([^\'"]*)[\'"]\s*\)',
            # print с несколькими аргументами
            r'(obfuscated_var_\d+)\s*\(.*?\)'
        ],
        'open': [
            # open с одним или двумя строковыми аргументами
            r'(obfuscated_var_\d+)\s*\(\s*[\'"]([^\'"]*)[\'"]\s*(?:,\s*[\'"]([^\'"]*)[\'"])?\s*\)'
        ],
        'range': [
            # range с одним или несколькими числовыми аргументами
            r'(obfuscated_var_\d+)\s*\(\s*\d+\s*(?:,\s*\d+\s*)?(?:,\s*\d+\s*)?\)'
        ],
        'int': [
            # int с одним аргументом
            r'(obfuscated_var_\d+)\s*\(\s*[\'"]?(\d+)[\'"]?\s*\)'
        ],
        'str': [
            # str с различными аргументами
            r'(obfuscated_var_\d+)\s*\(\s*[^)]*\)'
        ],
        'len': [
            # len с одним аргументом
            r'(obfuscated_var_\d+)\s*\(\s*\w+\s*\)'
        ],
        'isinstance': [
            # isinstance с двумя аргументами
            r'(obfuscated_var_\d+)\s*\(\s*\w+\s*,\s*\w+\s*\)'
        ],
        'getattr': [
            # getattr с двумя или тремя аргументами
            r'(obfuscated_var_\d+)\s*\(\s*\w+\s*,\s*[\'"]([^\'"]*)[\'"](?:\s*,\s*[^)]*)?\s*\)'
        ]
    }
    
    # Ищем использование функций
    for func_name, patterns in function_patterns.items():
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                if isinstance(match, tuple):
                    var_name = match[0]
                    normal_names[var_name] = func_name
    
    # Ищем присваивания и сравнения, которые могут указывать на типы и константы
    type_patterns = {
        'True': r'(obfuscated_var_\d+)\s*=\s*True',
        'False': r'(obfuscated_var_\d+)\s*=\s*False',
        'None': r'(obfuscated_var_\d+)\s*=\s*None',
        'dict': r'(obfuscated_var_\d+)\s*=\s*\{\}',
        'list': r'(obfuscated_var_\d+)\s*=\s*\[\]',
        'tuple': r'(obfuscated_var_\d+)\s*=\s*\(\)'
    }
    
    for type_name, pattern in type_patterns.items():
        matches = re.findall(pattern, code)
        for var_name in matches:
            normal_names[var_name] = type_name
    
    return normal_names

def analyze_function_usage(code):
    """
    Анализирует использование обфусцированных функций для определения их назначения
    """
    function_info = {}
    
    # Ищем определения функций
    function_pattern = r'def (obfuscated_(?:var|func)_\d+)\s*\(([^)]*)\):'
    function_defs = re.findall(function_pattern, code)
    
    for func_name, args in function_defs:
        # Извлекаем тело функции
        func_def_index = code.find(f"def {func_name}")
        if func_def_index == -1:
            continue
        
        # Ищем начало тела функции
        body_start = code.find(':', func_def_index) + 1
        
        # Ищем конец тела функции (до следующего определения функции или конца файла)
        next_def = code.find('\ndef ', body_start)
        if next_def == -1:
            body_end = len(code)
        else:
            body_end = next_def
        
        func_body = code[body_start:body_end]
        
        # Определяем назначение функции по содержимому
        purpose = "unknown"
        
        # Проверяем наличие декоратора async перед функцией
        if 'async' in code[max(0, func_def_index-10):func_def_index].split():
            purpose = "async_function"
        
        # Проверяем сигнатуру функции
        if '*' in args and '**' in args:
            purpose = "wrapper"
        elif re.search(r'\bself\b', args):
            purpose = "method"
        
        # Проверяем содержимое функции для уточнения назначения
        if 'yield' in func_body:
            purpose = "generator"
        elif 'return' in func_body and len(func_body.split('return')) > 2:
            # Если в функции несколько return, это может быть условная логика
            purpose = "conditional_logic"
        elif 'if' in func_body and 'else' in func_body:
            purpose = "conditional_logic"
        elif re.search(r'for\s+\w+\s+in', func_body):
            purpose = "iterator_function"
        elif 'try' in func_body and 'except' in func_body:
            purpose = "exception_handler"
        elif re.search(r'await\s+', func_body):
            purpose = "async_function"
        
        function_info[func_name] = {
            'args': args.strip(),
            'purpose': purpose,
            'body_preview': func_body[:100].strip() + '...' if len(func_body) > 100 else func_body.strip()
        }
    
    return function_info

def map_variables_to_builtins(code):
    """
    Создает сопоставление между обфусцированными переменными и встроенными именами Python
    """
    # Сначала анализируем структуру кортежа
    tuple_content, values_content = analyze_tuple_structure(code)
    if not tuple_content:
        return {}
    
    # Извлекаем первичное сопоставление из кортежа
    mapping = extract_builtin_mapping(tuple_content)
    
    # Улучшаем сопоставление путем анализа использования переменных
    normal_names = scan_for_normal_names(code)
    
    # Объединяем результаты, отдавая приоритет анализу использования
    for var_name, function_name in normal_names.items():
        mapping[var_name] = function_name
    
    return mapping

def deobfuscate_variables(code, mapping):
    """
    Заменяет обфусцированные имена переменных на их реальные имена
    """
    for var_name, real_name in mapping.items():
        # Заменяем переменную только если это отдельное слово (с границами слова)
        code = re.sub(r'\b' + re.escape(var_name) + r'\b', real_name, code)
    
    return code

def simplify_code_structure(code):
    """
    Упрощает структуру кода, удаляя избыточные конструкции
    """
    # Удаляем кортеж переопределений в начале файла
    tuple_start = code.find('(')
    if tuple_start >= 0:
        # Ищем конец всего блока переопределений
        assignment_pattern = r'\)\s*=\s*\('
        assignment_match = re.search(assignment_pattern, code)
        if assignment_match:
            values_start = tuple_end = assignment_match.start() + tuple_start
            
            # Ищем закрывающую скобку второго кортежа
            depth = 1
            values_end = values_start + assignment_match.end() - assignment_match.start() + 1
            while depth > 0 and values_end < len(code):
                if code[values_end] == '(':
                    depth += 1
                elif code[values_end] == ')':
                    depth -= 1
                values_end += 1
            
            if depth == 0:
                # Удаляем весь блок переопределений
                code = code[values_end:].strip()
    
    return code

def cleanup_code(code):
    """
    Выполняет общую очистку кода
    """
    # Удаляем избыточные пустые строки
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    # Удаляем комментарии с обфусцированными именами
    code = re.sub(r'#\s*obfuscated_(?:var|func)_\d+.*$', '', code, flags=re.MULTILINE)
    
    # Удаляем строки, которые только присваивают значения переопределенным функциям
    code = re.sub(r'^[a-zA-Z0-9_]+\s*=\s*[a-zA-Z0-9_]+\s*$', '', code, flags=re.MULTILINE)
    
    # Удаляем избыточные пустые строки после предыдущих операций
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    return code

def rename_obfuscated_functions(code, function_info):
    """
    Переименовывает обфусцированные функции на более понятные имена на основе их назначения
    """
    # Создаем словарь замен для функций
    function_mapping = {}
    counts = {}
    
    for func_name, info in function_info.items():
        purpose = info['purpose']
        
        # Инициализируем счетчик, если необходимо
        if purpose not in counts:
            counts[purpose] = 1
        
        # Создаем новое имя функции на основе ее назначения
        new_name = f"{purpose}_{counts[purpose]}"
        counts[purpose] += 1
        
        # Добавляем в словарь замен
        function_mapping[func_name] = new_name
    
    # Применяем замены
    for old_name, new_name in function_mapping.items():
        # Заменяем только целые имена, не части других имен
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def deobfuscate_layer8(input_file, output_file):
    """
    Основная функция деобфускации слоя 8
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Создаем сопоставление обфусцированных переменных и встроенных имен
    print("Поиск сопоставлений между обфусцированными переменными и встроенными именами...")
    mapping = map_variables_to_builtins(code)
    print(f"Найдено {len(mapping)} сопоставлений переменных со встроенными функциями")
    
    # Анализируем функции для их лучшего понимания
    print("Анализ обфусцированных функций...")
    function_info = analyze_function_usage(code)
    print(f"Проанализировано {len(function_info)} обфусцированных функций")
    
    # Применяем деобфускацию переменных
    print("Замена обфусцированных переменных на их реальные имена...")
    deobfuscated_code = deobfuscate_variables(code, mapping)
    
    # Упрощаем структуру кода
    print("Упрощение структуры кода...")
    simplified_code = simplify_code_structure(deobfuscated_code)
    
    # Переименовываем функции
    print("Переименование обфусцированных функций...")
    renamed_code = rename_obfuscated_functions(simplified_code, function_info)
    
    # Очищаем код
    print("Финальная очистка кода...")
    cleaned_code = cleanup_code(renamed_code)
    
    # Записываем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_code)
    
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")
    
    # Вывод статистики о заменах
    print("\nСтатистика замен:")
    print(f"- Заменено {len(mapping)} обфусцированных переменных")
    print(f"- Заменено {len(function_info)} обфусцированных функций")
    
    # Группировка функций по их назначению
    purposes = {}
    for info in function_info.values():
        purpose = info['purpose']
        if purpose not in purposes:
            purposes[purpose] = 0
        purposes[purpose] += 1
    
    print("\nТипы обнаруженных функций:")
    for purpose, count in purposes.items():
        print(f"- {purpose}: {count}")

if __name__ == "__main__":
    deobfuscate_layer8("layer8.py", "layer9.py") 