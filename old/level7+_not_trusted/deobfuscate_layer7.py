import re
import ast
import tokenize
from io import BytesIO

def evaluate_complex_expr(expr_str):
    """Пытается вычислить сложные выражения"""
    try:
        # Попытка использовать ast.literal_eval для безопасной оценки выражения
        return ast.literal_eval(expr_str)
    except (ValueError, SyntaxError):
        try:
            # Если не удалось, пробуем с eval (небезопасно, но эффективно)
            return eval(expr_str)
        except:
            # Если и это не помогло, возвращаем None
            return None

def simplify_chr_expressions(code):
    """Заменяет сложные выражения с chr() на их фактические символы"""
    
    def replace_chr_call(match):
        expr = match.group(1)
        try:
            # Пытаемся вычислить выражение внутри chr()
            value = evaluate_complex_expr(expr)
            if value is not None and isinstance(value, int):
                return f'"{chr(value)}"'
        except:
            pass
        # Если не можем вычислить, оставляем как есть
        return f'chr({expr})'
    
    # Ищем вызовы chr() с выражениями внутри
    pattern = r'chr\(([^)]+)\)'
    return re.sub(pattern, replace_chr_call, code)

def simplify_int_expressions(code):
    """Заменяет вызовы int() с различными системами счисления на числовые значения"""
    
    def replace_int_call(match):
        args = match.group(1)
        try:
            # Пытаемся вычислить int() выражение
            result = eval(f"int({args})")
            return str(result)
        except:
            # Если не можем вычислить, оставляем как есть
            return f'int({args})'
    
    # Ищем вызовы int() с аргументами
    pattern = r'int\(([^)]+)\)'
    return re.sub(pattern, replace_int_call, code)

def simplify_getattr_calls(code):
    """Упрощает вызовы getattr() когда второй аргумент - строка или может быть вычислен"""
    
    def replace_getattr_call(match):
        obj = match.group(1)
        attr_expr = match.group(2)
        
        # Проверяем, является ли attr_expr строкой или выражением, которое можно вычислить
        try:
            if attr_expr.startswith('"') or attr_expr.startswith("'"):
                # Если это строковый литерал, просто извлекаем значение
                attr = ast.literal_eval(attr_expr)
                return f"{obj}.{attr}"
            elif attr_expr.startswith('getattr('):
                # Оставляем сложные вложенные getattr() как есть
                return f"getattr({obj}, {attr_expr})"
            elif 'decode' in attr_expr and 'utf-8' in attr_expr:
                # Пробуем обработать случаи с декодированием
                return f"getattr({obj}, {attr_expr})"
            else:
                # Пытаемся вычислить значение выражения
                attr = evaluate_complex_expr(attr_expr)
                if isinstance(attr, str):
                    return f"{obj}.{attr}"
        except:
            pass
        
        # Если не удалось обработать, оставляем как есть
        return f"getattr({obj}, {attr_expr})"
    
    # Ищем вызовы getattr() с двумя аргументами
    pattern = r'getattr\(([^,]+),\s*([^,)]+)\)'
    result = re.sub(pattern, replace_getattr_call, code)
    
    # Если были изменения, повторяем процесс (для вложенных вызовов)
    if result != code:
        return simplify_getattr_calls(result)
    return result

def extract_u1KQ2EguJKQ7_function(code):
    """Извлекает функцию u1KQ2EguJKQ7 для последующего анализа"""
    pattern = r'def u1KQ2EguJKQ7\(UWdGO89tcyS7\):(.*?)return bytes'
    match = re.search(pattern, code, re.DOTALL)
    
    if match:
        # Дополняем найденную функцию, чтобы получить полный код
        function_body = match.group(0) + '\n    ]\n)'
        # Возвращаем код функции
        return function_body
    return None

def create_mock_objects_for_u1KQ2EguJKQ7():
    """
    Создает заглушки для объектов, используемых в функции u1KQ2EguJKQ7
    для возможности её выполнения в изолированной среде
    """
    mock_code = """
class MockBytes:
    def __init__(self, data=b''):
        self.data = data if isinstance(data, bytes) else bytes(data)
    
    def decode(self, encoding):
        return self.data.decode(encoding)

def mock_chr(code):
    return chr(code)

def mock_int(*args):
    return int(*args)

# Другие необходимые заглушки можно добавить здесь
"""
    return mock_code

def extract_xor_key_from_u1KQ2EguJKQ7(code):
    """
    Пытается извлечь XOR ключ из функции u1KQ2EguJKQ7 путем анализа кода
    """
    # Извлекаем функцию u1KQ2EguJKQ7
    u1KQ2EguJKQ7_code = extract_u1KQ2EguJKQ7_function(code)
    if not u1KQ2EguJKQ7_code:
        return None
    
    # Анализируем функцию и пытаемся понять формат ключа
    # Ищем ключевую строку, которая определяет индексацию в массиве ключей
    # Эта строка обычно содержит операцию взятия по модулю, например:
    # key[i % len(key)]
    modulo_pattern = r'(\w+)\s*%\s*int\([^)]+\)'
    modulo_matches = re.findall(modulo_pattern, u1KQ2EguJKQ7_code)
    
    if modulo_matches:
        variable_name = modulo_matches[0]
        # Теперь ищем, где этот индекс используется для доступа к массиву
        array_access_pattern = fr'\[\s*{variable_name}\s*%[^\]]+\]'
        array_matches = re.findall(array_access_pattern, u1KQ2EguJKQ7_code)
        
        if array_matches:
            # Нашли доступ к массиву, теперь нужно найти сам массив
            # Это сложно и зависит от конкретной обфускации
            # Для простоты рассмотрим случай, когда массив определен прямо в коде
            
            # Ищем массив с числами (упрощенный подход)
            array_pattern = r'\[\s*int\([^)]+\),\s*int\([^)]+\),.*?\]'
            array_def_match = re.search(array_pattern, u1KQ2EguJKQ7_code, re.DOTALL)
            
            if array_def_match:
                array_def = array_def_match.group(0)
                try:
                    # Осторожно! Использование eval небезопасно
                    # Но для деобфускации иногда необходимо
                    xor_key = eval(array_def)
                    return xor_key
                except:
                    print("Не удалось вычислить XOR ключ из найденного массива")
    
    # Более общий подход: ищем все int() вызовы и пытаемся их вычислить
    int_pattern = r'int\(([^)]+)\)'
    int_matches = re.findall(int_pattern, u1KQ2EguJKQ7_code)
    
    if int_matches:
        # Пытаемся вычислить все найденные int() выражения
        xor_key = []
        for int_expr in int_matches:
            try:
                value = eval(f"int({int_expr})")
                xor_key.append(value)
            except:
                continue
        
        if xor_key:
            return xor_key
    
    # Если не удалось найти ключ стандартными методами,
    # попробуем проанализировать строки в функции и найти потенциальные константы
    hex_pattern = r'0x[0-9a-fA-F]+'
    hex_matches = re.findall(hex_pattern, u1KQ2EguJKQ7_code)
    
    if hex_matches:
        xor_key = []
        for hex_value in hex_matches:
            try:
                value = int(hex_value, 16)
                xor_key.append(value)
            except:
                continue
        
        if xor_key:
            return xor_key
    
    # Если ничего не нашли, возвращаем None
    return None

def reconstruct_xor_key(function_code):
    """
    Анализирует функцию u1KQ2EguJKQ7 и пытается извлечь XOR ключ
    """
    # Для начала попробуем использовать специализированную функцию
    xor_key = extract_xor_key_from_u1KQ2EguJKQ7(function_code)
    if xor_key:
        return xor_key
    
    # Если специализированный метод не сработал, используем общий подход
    try:
        # Ищем массив с числами - это обычно ключ для XOR
        key_array_pattern = r'\[\s*int\([^)]+\),\s*int\([^)]+\),.*?\]'
        key_match = re.search(key_array_pattern, function_code, re.DOTALL)
        
        if key_match:
            key_array_str = key_match.group(0)
            try:
                # Пытаемся выполнить код, чтобы получить значения
                xor_key = eval(key_array_str)
                return xor_key
            except Exception as e:
                print(f"Не удалось вычислить XOR ключ напрямую: {e}")
                # Если не удалось, извлекаем отдельные int() выражения
                int_pattern = r'int\(([^)]+)\)'
                int_matches = re.findall(int_pattern, key_array_str)
                
                if int_matches:
                    key_values = []
                    for match in int_matches:
                        try:
                            value = eval(f"int({match})")
                            key_values.append(value)
                        except:
                            continue
                    
                    if key_values:
                        return key_values
        
        # Если не нашли явный массив, пробуем найти упоминания чисел
        int_values_pattern = r'int\(([^)]+)\)'
        int_matches = re.findall(int_values_pattern, function_code)
        
        if int_matches:
            key_values = []
            for match in int_matches:
                try:
                    value = eval(f"int({match})")
                    key_values.append(value)
                except:
                    continue
            
            if key_values:
                return key_values
    
    except Exception as e:
        print(f"Ошибка при извлечении XOR ключа: {e}")
    
    # Если не удалось извлечь ключ, возвращаем None
    return None

def implement_xor_decode_function(xor_key=None):
    """
    Создает функцию для декодирования XOR-шифрованных строк
    """
    if xor_key is None:
        # Если ключ не удалось извлечь, создаем заглушку
        return """
def xor_decode(data):
    # Заглушка для декодирования
    # Необходимо вручную проанализировать и реализовать логику декодирования
    return data
"""
    else:
        # Если удалось извлечь ключ, создаем реальную функцию декодирования
        return f"""
def xor_decode(data):
    # Функция декодирования на основе извлеченного ключа
    key = {xor_key}
    if not isinstance(data, bytes):
        if isinstance(data, str):
            data = data.encode('utf-8')
        else:
            data = bytes(data)
    
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    
    return bytes(result)
"""

def implement_string_decoder(code, xor_key=None):
    """
    Реализует декодер строк на основе изученной логики обфускации
    """
    # Создаем функцию для декодирования
    decode_function = implement_xor_decode_function(xor_key)
    
    # Добавляем функцию в начало кода
    code = decode_function + "\n\n" + code
    
    # Заменяем вызовы u1KQ2EguJKQ7 на вызовы нашей функции xor_decode
    def decode_encoded_string(match):
        encoded_bytes = match.group(1)
        return f"xor_decode({encoded_bytes})"
    
    pattern = r'u1KQ2EguJKQ7\((b"[^"]+"|b\'[^\']+\')\)'
    modified_code = re.sub(pattern, decode_encoded_string, code)
    
    # Также ищем более сложные случаи, когда параметр не является буквальным строковым литералом
    complex_pattern = r'u1KQ2EguJKQ7\(([^)]+)\)'
    result = re.sub(complex_pattern, lambda m: f"xor_decode({m.group(1)})" if not (m.group(1).startswith('b"') or m.group(1).startswith("b'")) else m.group(0), modified_code)
    
    # Если нет изменений, возвращаем модифицированный код
    if result == modified_code:
        return modified_code
    
    # Если были изменения, снова применяем простой паттерн для буквальных строк
    return re.sub(pattern, decode_encoded_string, result)

def analyze_decoding_function(code):
    """Анализирует функцию декодирования для понимания логики"""
    function_code = extract_u1KQ2EguJKQ7_function(code)
    
    if function_code:
        print("Извлечена функция декодирования")
        # Проверяем, использует ли функция XOR шифрование
        is_xor = "^" in function_code
        
        if is_xor:
            print("Анализ XOR шифрования...")
            # Пытаемся извлечь ключ XOR
            xor_key = reconstruct_xor_key(function_code)
            return is_xor, xor_key
        
        return is_xor, None
    
    return False, None

def remove_obfuscated_variable_names(code):
    """
    Заменяет обфусцированные имена переменных на более понятные
    """
    # Находим все странные имена переменных (обычно содержат случайные символы)
    var_pattern = r'\b[a-zA-Z0-9_]{10,}\b'
    var_matches = re.findall(var_pattern, code)
    
    # Создаем словарь замен
    replacements = {}
    for i, var in enumerate(set(var_matches)):
        if var.startswith('__') and var.endswith('__'):
            continue  # Пропускаем системные имена
        
        if var in code.split('def '):
            # Это функция
            replacements[var] = f"obfuscated_func_{i}"
        else:
            # Это переменная
            replacements[var] = f"obfuscated_var_{i}"
    
    # Заменяем имена в коде
    for old_name, new_name in replacements.items():
        # Используем регулярное выражение для замены только полных имен переменных
        code = re.sub(rf'\b{re.escape(old_name)}\b', new_name, code)
    
    return code

def cleanup_code(code):
    """
    Выполняет общую очистку кода от остаточных артефактов обфускации
    """
    # Удаляем избыточные переносы строк
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    # Удаляем комментарии вида # ENCODED_STRING
    code = re.sub(r'# ENCODED_STRING.*\n', '', code)
    
    return code

def deobfuscate_layer7(input_file, output_file):
    """Основная функция деобфускации"""
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Анализируем функцию декодирования
    is_xor, xor_key = analyze_decoding_function(code)
    
    # Применяем различные трансформации
    code = simplify_chr_expressions(code)
    code = simplify_int_expressions(code)
    code = simplify_getattr_calls(code)
    
    if is_xor:
        print("Обнаружено XOR-кодирование строк")
        if xor_key:
            print(f"Извлечен XOR ключ: {xor_key}")
        else:
            print("Не удалось извлечь XOR ключ автоматически")
        
        # Реализуем декодер на основе извлеченного ключа
        code = implement_string_decoder(code, xor_key)
    
    # Дополнительная очистка и улучшение кода
    code = remove_obfuscated_variable_names(code)
    code = cleanup_code(code)
    
    # Записываем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"Деобфускация завершена. Результат сохранен в {output_file}")

if __name__ == "__main__":
    deobfuscate_layer7("layer7.py", "layer8.py") 