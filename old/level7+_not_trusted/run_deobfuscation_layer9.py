#!/usr/bin/env python3

import os
import subprocess
import sys
import re

def print_colored(text, color="green"):
    """Вывод текста с цветом"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['green'])}{text}{colors['reset']}")

def run_command(command, description=None):
    """Запускает команду и печатает вывод"""
    if description:
        print_colored(f"{description}...", "blue")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print_colored("Вывод команды:", "yellow")
        print(result.stdout)
        
        if result.stderr:
            print_colored("Ошибки:", "red")
            print(result.stderr)
        
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print_colored(f"Ошибка при выполнении команды: {e}", "red")
        print("Вывод команды:")
        print(e.stdout)
        print("Ошибки:")
        print(e.stderr)
        return False, str(e)

def print_header(text, width=70, char="="):
    """Печатает заголовок с рамкой"""
    print(char * width)
    print(text.center(width))
    print(char * width)

def analyze_layer9_file():
    """Анализирует файл layer9.py и выводит основную информацию"""
    if not os.path.exists("layer9.py"):
        print_colored("Ошибка: Файл layer9.py не найден", "red")
        return
    
    # Подсчитываем количество строк
    with open("layer9.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print_colored(f"Файл layer9.py содержит {len(lines)} строк", "blue")
    
    # Подсчитываем количество обфусцированных переменных
    with open("layer9.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    var_pattern = r'obfuscated_var_\d+'
    var_matches = re.findall(var_pattern, content)
    unique_vars = set(var_matches)
    
    print_colored(f"Найдено {len(unique_vars)} уникальных обфусцированных переменных", "blue")
    
    # Подсчитываем количество строковых конкатенаций
    concat_pattern = r'("[^"\\]*(?:\\.[^"\\]*)*"\s*\+\s*)+("[^"\\]*(?:\\.[^"\\]*)*")'
    concat_matches = re.findall(concat_pattern, content)
    
    print_colored(f"Найдено {len(concat_matches)} строковых конкатенаций", "blue")
    
    # Подсчитываем количество шестнадцатеричных и восьмеричных escape-последовательностей
    hex_pattern = r'\\x[0-9a-fA-F]{2}'
    hex_matches = re.findall(hex_pattern, content)
    
    octal_pattern = r'\\0[0-7]{1,2}'
    octal_matches = re.findall(octal_pattern, content)
    
    print_colored(f"Найдено {len(hex_matches)} шестнадцатеричных и {len(octal_matches)} восьмеричных escape-последовательностей", "blue")
    
    # Подсчитываем количество вызовов ord()
    ord_pattern = r'ord\(\s*["\'][^"\']*["\']\s*\)'
    ord_matches = re.findall(ord_pattern, content)
    
    print_colored(f"Найдено {len(ord_matches)} вызовов ord()", "blue")
    
    # Подсчитываем количество вызовов getattr()
    getattr_pattern = r'getattr\(\s*[^,]+\s*,\s*[^,)]+(?:\s*,\s*[^)]+)?\s*\)'
    getattr_matches = re.findall(getattr_pattern, content)
    
    print_colored(f"Найдено {len(getattr_matches)} вызовов getattr()", "blue")

def main():
    print_header("ДЕОБФУСКАЦИЯ СЛОЯ 9")
    
    # Проверяем наличие файлов
    if not os.path.exists("layer9.py"):
        print_colored("Ошибка: Файл layer9.py не найден", "red")
        return
    
    if not os.path.exists("deobfuscate_layer9.py"):
        print_colored("Ошибка: Файл deobfuscate_layer9.py не найден", "red")
        return
    
    # Анализируем файл layer9.py
    print_colored("Анализ файла layer9.py", "blue")
    analyze_layer9_file()
    
    # Запускаем деобфускацию
    print_colored("\nЗапуск процесса деобфускации", "blue")
    success, output = run_command(
        [sys.executable, "deobfuscate_layer9.py"],
        "Запуск деобфускатора слоя 9"
    )
    
    if not success:
        print_colored("Процесс деобфускации завершился с ошибкой", "red")
        return
    
    # Проверяем результат
    if os.path.exists("layer10.py"):
        # Подсчитываем статистику
        layer9_size = os.path.getsize("layer9.py")
        layer10_size = os.path.getsize("layer10.py")
        
        print_colored("\nСтатистика результатов:", "green")
        print(f"- Размер слоя 9: {layer9_size} байт")
        print(f"- Размер слоя 10: {layer10_size} байт")
        print(f"- Разница: {layer10_size - layer9_size:+d} байт ({(layer10_size / layer9_size * 100):.1f}%)")
        
        # Анализируем улучшения
        with open("layer9.py", 'r', encoding='utf-8') as f:
            content9 = f.read()
        
        with open("layer10.py", 'r', encoding='utf-8') as f:
            content10 = f.read()
        
        var_pattern = r'obfuscated_var_\d+'
        var_matches9 = re.findall(var_pattern, content9)
        var_matches10 = re.findall(var_pattern, content10)
        
        print(f"- Обфусцированные переменные: {len(var_matches9)} -> {len(var_matches10)} ({len(var_matches10) - len(var_matches9):+d})")
        
        concat_pattern = r'("[^"\\]*(?:\\.[^"\\]*)*"\s*\+\s*)+("[^"\\]*(?:\\.[^"\\]*)*")'
        concat_matches9 = re.findall(concat_pattern, content9)
        concat_matches10 = re.findall(concat_pattern, content10)
        
        print(f"- Строковые конкатенации: {len(concat_matches9)} -> {len(concat_matches10)} ({len(concat_matches10) - len(concat_matches9):+d})")
        
        getattr_pattern = r'getattr\(\s*[^,]+\s*,\s*[^,)]+(?:\s*,\s*[^)]+)?\s*\)'
        getattr_matches9 = re.findall(getattr_pattern, content9)
        getattr_matches10 = re.findall(getattr_pattern, content10)
        
        print(f"- Вызовы getattr(): {len(getattr_matches9)} -> {len(getattr_matches10)} ({len(getattr_matches10) - len(getattr_matches9):+d})")
        
        print_colored("\nДеобфускация успешно завершена!", "green")
        print_colored(f"Результат сохранен в файл: layer10.py", "green")
        print_colored("Для продолжения деобфускации используйте файл layer10.py", "green")
    else:
        print_colored("Ошибка: Файл layer10.py не был создан", "red")

if __name__ == "__main__":
    main() 