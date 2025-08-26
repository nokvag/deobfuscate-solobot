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

def analyze_layer8_file():
    """Анализирует файл layer8.py и выводит основную информацию"""
    if not os.path.exists("layer8.py"):
        print_colored("Ошибка: Файл layer8.py не найден", "red")
        return
    
    # Подсчитываем количество строк
    with open("layer8.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print_colored(f"Файл layer8.py содержит {len(lines)} строк", "blue")
    
    # Подсчитываем количество обфусцированных переменных
    with open("layer8.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    var_pattern = r'obfuscated_var_\d+'
    var_matches = re.findall(var_pattern, content)
    unique_vars = set(var_matches)
    
    print_colored(f"Найдено {len(unique_vars)} уникальных обфусцированных переменных", "blue")
    
    # Подсчитываем количество обфусцированных функций
    func_pattern = r'def (obfuscated_(?:var|func)_\d+)'
    func_matches = re.findall(func_pattern, content)
    unique_funcs = set(func_matches)
    
    print_colored(f"Найдено {len(unique_funcs)} уникальных обфусцированных функций", "blue")

def main():
    print_header("ДЕОБФУСКАЦИЯ СЛОЯ 8")
    
    # Проверяем наличие файлов
    if not os.path.exists("layer8.py"):
        print_colored("Ошибка: Файл layer8.py не найден", "red")
        return
    
    if not os.path.exists("deobfuscate_layer8.py"):
        print_colored("Ошибка: Файл deobfuscate_layer8.py не найден", "red")
        return
    
    # Анализируем файл layer8.py
    print_colored("Анализ файла layer8.py", "blue")
    analyze_layer8_file()
    
    # Запускаем деобфускацию
    print_colored("\nЗапуск процесса деобфускации", "blue")
    success, output = run_command(
        [sys.executable, "deobfuscate_layer8.py"],
        "Запуск деобфускатора слоя 8"
    )
    
    if not success:
        print_colored("Процесс деобфускации завершился с ошибкой", "red")
        return
    
    # Проверяем результат
    if os.path.exists("layer9.py"):
        # Подсчитываем статистику
        layer8_size = os.path.getsize("layer8.py")
        layer9_size = os.path.getsize("layer9.py")
        
        print_colored("\nСтатистика результатов:", "green")
        print(f"- Размер слоя 8: {layer8_size} байт")
        print(f"- Размер слоя 9: {layer9_size} байт")
        print(f"- Разница: {layer9_size - layer8_size} байт ({(layer9_size / layer8_size * 100):.1f}%)")
        
        print_colored("\nДеобфускация успешно завершена!", "green")
        print_colored(f"Результат сохранен в файл: layer9.py", "green")
        print_colored("Для продолжения деобфускации используйте файл layer9.py", "green")
    else:
        print_colored("Ошибка: Файл layer9.py не был создан", "red")

if __name__ == "__main__":
    main() 