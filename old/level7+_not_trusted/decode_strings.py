#!/usr/bin/env python3

import re
import sys
import os
import importlib.util

def load_decode_function(decode_module_path):
    """Загружает функцию декодирования из модуля"""
    if not os.path.exists(decode_module_path):
        print(f"Ошибка: Файл {decode_module_path} не найден")
        return None
    
    try:
        spec = importlib.util.spec_from_file_location("decode_module", decode_module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'decode_xor'):
            return module.decode_xor
        
        print(f"Ошибка: В модуле {decode_module_path} не найдена функция decode_xor")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке модуля декодирования: {e}")
        return None

def find_encoded_strings(code):
    """Находит зашифрованные строки в коде"""
    encoded_pattern = r'u1KQ2EguJKQ7\((b"[^"]+"|b\'[^\']+\')\)'
    encoded_matches = re.findall(encoded_pattern, code)
    
    if encoded_matches:
        print(f"Найдено {len(encoded_matches)} зашифрованных строк")
        return encoded_matches
    
    print("Зашифрованные строки не найдены")
    return []

def decode_strings(code, decode_function):
    """Декодирует зашифрованные строки в коде"""
    encoded_strings = find_encoded_strings(code)
    
    if not encoded_strings:
        return code
    
    # Создаем словарь замен
    replacements = {}
    for i, encoded_str in enumerate(encoded_strings):
        try:
            # Преобразуем строку в объект bytes
            data = eval(encoded_str)
            # Декодируем данные
            decoded = decode_function(data)
            
            try:
                # Пытаемся декодировать как UTF-8 строку
                decoded_str = decoded.decode('utf-8')
                print(f"Строка {i+1}: {encoded_str[:30]}... -> {decoded_str[:50]}...")
                replacements[f"u1KQ2EguJKQ7({encoded_str})"] = f'"{decoded_str}"'
            except UnicodeDecodeError:
                # Если не удается декодировать как UTF-8, оставляем как bytes
                print(f"Строка {i+1}: {encoded_str[:30]}... -> [Двоичные данные]")
                replacements[f"u1KQ2EguJKQ7({encoded_str})"] = f"bytes({decoded})"
        except Exception as e:
            print(f"Ошибка при декодировании строки {i+1}: {e}")
    
    # Применяем замены
    for encoded, decoded in replacements.items():
        code = code.replace(encoded, decoded)
    
    return code

def main():
    if len(sys.argv) < 4:
        print("Использование: python decode_strings.py <путь_к_обфусцированному_файлу> <путь_к_модулю_декодирования> <путь_к_выходному_файлу>")
        return
    
    input_file = sys.argv[1]
    decode_module_path = sys.argv[2]
    output_file = sys.argv[3]
    
    if not os.path.exists(input_file):
        print(f"Ошибка: Входной файл {input_file} не найден")
        return
    
    # Загружаем функцию декодирования
    decode_function = load_decode_function(decode_module_path)
    if not decode_function:
        return
    
    # Читаем содержимое входного файла
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Декодируем строки
    decoded_code = decode_strings(code, decode_function)
    
    # Записываем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decoded_code)
    
    print(f"Декодированный код сохранен в {output_file}")

if __name__ == "__main__":
    main() 