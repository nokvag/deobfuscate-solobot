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

def analyze_layer10_file():
    """Анализирует файл layer10.py и выводит основную информацию"""
    if not os.path.exists("layer10.py"):
        print_colored("Ошибка: Файл layer10.py не найден", "red")
        return
    
    # Подсчитываем количество строк
    with open("layer10.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print_colored(f"Файл layer10.py содержит {len(lines)} строк", "blue")
    
    # Подсчитываем количество переменных var_X
    with open("layer10.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    var_pattern = r'var_\d+'
    var_matches = re.findall(var_pattern, content)
    unique_vars = set(var_matches)
    
    print_colored(f"Найдено {len(unique_vars)} уникальных переменных типа var_X", "blue")
    
    # Подсчитываем количество строковых конкатенаций
    concat_pattern = r'([\'"][^\'"]*[\'"])\s*\+\s*([\'"][^\'"]*[\'"])'
    concat_matches = re.findall(concat_pattern, content)
    
    print_colored(f"Найдено {len(concat_matches)} строковых конкатенаций", "blue")
    
    # Подсчитываем количество байтовых строк
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    bytes_matches = re.findall(bytes_pattern, content)
    
    print_colored(f"Найдено {len(bytes_matches)} байтовых строк", "blue")
    
    # Подсчитываем количество вызовов getattr
    getattr_pattern = r'getattr\([^,]+,\s*([^,)]+)'
    getattr_matches = re.findall(getattr_pattern, content)
    
    print_colored(f"Найдено {len(getattr_matches)} вызовов getattr()", "blue")
    
    # Подсчитываем количество функций conditional_logic_X
    func_pattern = r'(conditional_logic_\d+)'
    func_matches = re.findall(func_pattern, content)
    unique_funcs = set(func_matches)
    
    print_colored(f"Найдено {len(unique_funcs)} уникальных функций conditional_logic_X", "blue")

def main():
    print_header("ДЕОБФУСКАЦИЯ СЛОЯ 10")
    
    # Проверяем наличие файлов
    if not os.path.exists("layer10.py"):
        print_colored("Ошибка: Файл layer10.py не найден", "red")
        return
    
    if not os.path.exists("deobfuscate_layer10.py"):
        print_colored("Ошибка: Файл deobfuscate_layer10.py не найден", "red")
        return
    
    # Анализируем файл layer10.py
    print_colored("Анализ файла layer10.py", "blue")
    analyze_layer10_file()
    
    # Запускаем деобфускацию
    print_colored("\nЗапуск процесса деобфускации", "blue")
    success, output = run_command(
        [sys.executable, "deobfuscate_layer10.py"],
        "Запуск деобфускатора слоя 10"
    )
    
    if not success:
        print_colored("Процесс деобфускации завершился с ошибкой", "red")
        return
    
    # Проверяем результат
    if os.path.exists("layer11.py"):
        # Подсчитываем статистику
        layer10_size = os.path.getsize("layer10.py")
        layer11_size = os.path.getsize("layer11.py")
        
        print_colored("\nСтатистика результатов:", "green")
        print(f"- Размер слоя 10: {layer10_size} байт")
        print(f"- Размер слоя 11: {layer11_size} байт")
        print(f"- Разница: {layer11_size - layer10_size:+d} байт ({(layer11_size / layer10_size * 100):.1f}%)")
        
        # Анализируем улучшения
        with open("layer10.py", 'r', encoding='utf-8') as f:
            content10 = f.read()
        
        with open("layer11.py", 'r', encoding='utf-8') as f:
            content11 = f.read()
        
        # Подсчитываем количество переменных var_X до и после
        var_pattern = r'var_\d+'
        var_matches10 = re.findall(var_pattern, content10)
        var_matches11 = re.findall(var_pattern, content11)
        
        print(f"- Переменные var_X: {len(var_matches10)} → {len(var_matches11)} ({len(var_matches11) - len(var_matches10):+d})")
        
        # Подсчитываем количество строковых конкатенаций до и после
        concat_pattern = r'([\'"][^\'"]*[\'"])\s*\+\s*([\'"][^\'"]*[\'"])'
        concat_matches10 = re.findall(concat_pattern, content10)
        concat_matches11 = re.findall(concat_pattern, content11)
        
        print(f"- Строковые конкатенации: {len(concat_matches10)} → {len(concat_matches11)} ({len(concat_matches11) - len(concat_matches10):+d})")
        
        # Подсчитываем количество байтовых строк до и после
        bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
        bytes_matches10 = re.findall(bytes_pattern, content10)
        bytes_matches11 = re.findall(bytes_pattern, content11)
        
        print(f"- Байтовые строки: {len(bytes_matches10)} → {len(bytes_matches11)} ({len(bytes_matches11) - len(bytes_matches10):+d})")
        
        # Подсчитываем количество вызовов getattr до и после
        getattr_pattern = r'getattr\([^,]+,\s*([^,)]+)'
        getattr_matches10 = re.findall(getattr_pattern, content10)
        getattr_matches11 = re.findall(getattr_pattern, content11)
        
        print(f"- Вызовы getattr(): {len(getattr_matches10)} → {len(getattr_matches11)} ({len(getattr_matches11) - len(getattr_matches10):+d})")
        
        # Подсчитываем количество функций conditional_logic_X до и после
        func_pattern = r'(conditional_logic_\d+)'
        func_matches10 = re.findall(func_pattern, content10)
        func_matches11 = re.findall(func_pattern, content11)
        
        print(f"- Функции conditional_logic_X: {len(func_matches10)} → {len(func_matches11)} ({len(func_matches11) - len(func_matches10):+d})")
        
        print_colored("\nДеобфускация успешно завершена!", "green")
        print_colored(f"Результат сохранен в файл: layer11.py", "green")
        print_colored("Для продолжения деобфускации используйте файл layer11.py", "green")
    else:
        print_colored("Ошибка: Файл layer11.py не был создан", "red")

if __name__ == "__main__":
    main() 