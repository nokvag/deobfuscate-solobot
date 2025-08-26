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
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def decode_all_strings(code):
    """
    Декодирует все зашифрованные строки в коде
    """
    # Извлекаем ключ XOR
    xor_key = extract_xor_key(code)
    if not xor_key:
        print("Не удалось извлечь ключ XOR")
        return code
    
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
                return f'"{decoded_str}"'
            except UnicodeDecodeError:
                # Если не удалось декодировать напрямую, пробуем через XOR
                try:
                    decoded_bytes = decode_xor_data(byte_data, xor_key)
                    decoded_str = decoded_bytes.decode('utf-8')
                    return f'"{decoded_str}"'
                except UnicodeDecodeError:
                    return match.group(0)
        except Exception as e:
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
            
            # Применяем XOR декодирование
            decoded_bytes = decode_xor_data(byte_data, xor_key)
            
            try:
                decoded_str = decoded_bytes.decode('utf-8')
                return f'"{decoded_str}"'
            except UnicodeDecodeError:
                return match.group(0)
        except Exception as e:
            return match.group(0)
    
    # Заменяем вызовы unknown_1
    code = re.sub(unknown_pattern, unknown_replacer, code)
    
    return code

def clean_decode_calls(code):
    """
    Очищает вызовы decode('utf-8')
    """
    # Заменяем getattr(..., "decode", )('utf-8') на прямые строковые литералы
    decode_pattern = r'getattr\(([^,]+),\s*[\'"]decode[\'"],\s*\)\([\'"]utf-8[\'"]\)'
    
    def decode_replacer(match):
        try:
            obj_expr = match.group(1).strip()
            # Если это строковый литерал, просто возвращаем его без decode
            if obj_expr.startswith('"') and obj_expr.endswith('"'):
                return obj_expr
            # Иначе оставляем вызов как есть
            return match.group(0)
        except Exception:
            return match.group(0)
    
    code = re.sub(decode_pattern, decode_replacer, code)
    
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

def identify_module_variables(code):
    """
    Определяет и заменяет переменные, представляющие модули
    """
    # Словарь соответствий для модулей по характерным атрибутам или методам
    module_patterns = {
        r'(\w+)\.Event': 'asyncio',
        r'(\w+)\.run\(': 'asyncio',
        r'(\w+)\.all_tasks\(\)': 'asyncio',
        r'(\w+)\.TCPSite': 'aiohttp',
        r'(\w+)\.AppRunner': 'aiohttp',
        r'(\w+)\.path': 'os',
        r'(\w+)\.decode': 'bytes',
        r'(\w+)\.print': 'builtins',
        r'(\w+)\.router': 'app',
    }
    
    # Словарь для хранения идентифицированных переменных
    identified_vars = {}
    
    # Ищем совпадения по шаблонам
    for pattern, module_name in module_patterns.items():
        matches = re.findall(pattern, code)
        for var_name in matches:
            # Игнорируем уже известные модули
            if var_name not in identified_vars and var_name != module_name:
                identified_vars[var_name] = module_name
    
    # Заменяем переменные на имена модулей
    for var_name, module_name in identified_vars.items():
        # Используем границы слова, чтобы не заменять части других идентификаторов
        code = re.sub(r'\b' + re.escape(var_name) + r'\b', module_name, code)
    
    return code

def simplify_code_structures(code):
    """
    Упрощает различные структуры кода
    """
    # Удаляем ненужные скобки в простых выражениях
    code = re.sub(r'\(([a-zA-Z_][a-zA-Z0-9_]*)\)', r'\1', code)
    
    # Удаляем избыточные else-блоки с return
    code = re.sub(r'if (.+?):\s+return(.+?)\s+else:\s+return', r'if \1: return\2\n    return', code)
    
    # Упрощаем множественные вызовы getattr в стиле getattr(getattr(obj, "method")(...), "method2")
    # Это требует более сложного анализа и может быть реализовано с использованием AST
    
    return code

def cleanup_imports(code):
    """
    Очищает и упорядочивает импорты
    """
    # Находим все импорты
    import_pattern = r'(?:import|from) .+?(?:\n|$)'
    imports = re.findall(import_pattern, code)
    
    # Если импортов нет, возвращаем код без изменений
    if not imports:
        return code
    
    # Удаляем импорты из кода
    for imp in imports:
        code = code.replace(imp, '')
    
    # Удаляем дублирующиеся импорты
    unique_imports = sorted(set(imports))
    
    # Добавляем импорты в начало файла
    code = ''.join(unique_imports) + '\n' + code.lstrip()
    
    return code

def improve_variable_naming(code):
    """
    Улучшает именование переменных
    """
    # Словарь для известных шаблонов переменных
    var_patterns = {
        r'var_(\d+)\.router': 'app',
        r'var_(\d+)\.run\(': 'asyncio',
        r'var_(\d+)\.Event\(\)': 'event',
        r'var_(\d+)\.AppRunner': 'runner',
        r'var_(\d+)\.TCPSite': 'site',
        r'await var_(\d+)\(\)': 'task',
        r'var_(\d+)\.var_\d+': 'config',
    }
    
    # Словарь для замены переменных
    var_replacements = {}
    
    # Ищем совпадения по шаблонам
    for pattern, var_type in var_patterns.items():
        matches = re.findall(pattern, code)
        for var_id in matches:
            var_name = f'var_{var_id}'
            if var_name not in var_replacements:
                var_replacements[var_name] = f'{var_type}_{len(var_replacements) + 1}'
    
    # Заменяем переменные
    for old_name, new_name in var_replacements.items():
        code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, code)
    
    return code

def extract_meaningful_strings(code):
    """
    Анализирует строковые литералы для определения назначения переменных
    """
    # Шаблоны для определения контекста
    context_patterns = {
        r'"([^"]*webhook[^"]*)"': 'webhook',
        r'"([^"]*bot[^"]*)"': 'bot',
        r'"([^"]*token[^"]*)"': 'token',
        r'"([^"]*url[^"]*)"': 'url',
        r'"([^"]*host[^"]*)"': 'host',
        r'"([^"]*port[^"]*)"': 'port',
    }
    
    # Ищем контекстные строки
    context_matches = {}
    for pattern, context in context_patterns.items():
        matches = re.findall(pattern, code, re.IGNORECASE)
        if matches:
            for match in matches:
                # Ищем переменные перед или после строки
                var_before = re.findall(r'(var_\d+)\s*=\s*[\'"]' + re.escape(match) + '[\'"]', code)
                var_after = re.findall(r'[\'"]' + re.escape(match) + '[\'"].*?(var_\d+)', code)
                
                for var_name in var_before + var_after:
                    if var_name not in context_matches:
                        context_matches[var_name] = context
    
    # Заменяем переменные на основе найденного контекста
    for var_name, context in context_matches.items():
        code = re.sub(r'\b' + re.escape(var_name) + r'\b', f'{context}_{var_name[4:]}', code)
    
    return code

def deobfuscate_layer11(input_file, output_file):
    """
    Основная функция деобфускации слоя 11
    """
    # Загружаем код из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    original_size = len(code)
    print(f"Исходный размер файла: {original_size} байт")
    
    # Применяем функции деобфускации
    print("Декодирование всех строк...")
    code = decode_all_strings(code)
    
    print("Очистка вызовов decode('utf-8')...")
    code = clean_decode_calls(code)
    
    print("Упрощение вызовов getattr()...")
    code = simplify_getattr_calls(code)
    
    print("Определение переменных, представляющих модули...")
    code = identify_module_variables(code)
    
    print("Улучшение именования переменных...")
    code = improve_variable_naming(code)
    
    print("Извлечение осмысленных строк для контекста...")
    code = extract_meaningful_strings(code)
    
    print("Упрощение структур кода...")
    code = simplify_code_structures(code)
    
    print("Очистка и упорядочивание импортов...")
    code = cleanup_imports(code)
    
    # Сохраняем деобфусцированный код
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    new_size = len(code)
    print(f"Новый размер файла: {new_size} байт")
    print(f"Разница: {new_size - original_size} байт ({new_size / original_size * 100:.1f}%)")
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer11("layer11.py", "layer12.py") 