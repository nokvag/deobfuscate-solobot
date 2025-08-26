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

def analyze_layer11_file():
    """Анализирует файл layer11.py и выводит основную информацию"""
    if not os.path.exists("layer11.py"):
        print_colored("Ошибка: Файл layer11.py не найден", "red")
        return
    
    # Подсчитываем количество строк
    with open("layer11.py", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print_colored(f"Файл layer11.py содержит {len(lines)} строк", "blue")
    
    # Подсчитываем количество закодированных байтовых строк
    with open("layer11.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Байтовые строки
    bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
    bytes_matches = re.findall(bytes_pattern, content)
    
    print_colored(f"Найдено {len(bytes_matches)} байтовых строк", "blue")
    
    # Вызовы getattr
    getattr_pattern = r'getattr\([^,]+,\s*([^,)]+)'
    getattr_matches = re.findall(getattr_pattern, content)
    
    print_colored(f"Найдено {len(getattr_matches)} вызовов getattr()", "blue")
    
    # Вызовы xor_decode
    xor_decode_pattern = r'xor_decode\(([^)]+)\)'
    xor_decode_matches = re.findall(xor_decode_pattern, content)
    
    print_colored(f"Найдено {len(xor_decode_matches)} вызовов xor_decode()", "blue")
    
    # Вызовы unknown_1
    unknown_pattern = r'unknown_1\(([^)]+)\)'
    unknown_matches = re.findall(unknown_pattern, content)
    
    print_colored(f"Найдено {len(unknown_matches)} вызовов unknown_1()", "blue")
    
    # Переменные var_X
    var_pattern = r'var_\d+'
    var_matches = re.findall(var_pattern, content)
    unique_vars = set(var_matches)
    
    print_colored(f"Найдено {len(unique_vars)} уникальных переменных типа var_X", "blue")

def main():
    print_header("ДЕОБФУСКАЦИЯ СЛОЯ 11")
    
    # Проверяем наличие файлов
    if not os.path.exists("layer11.py"):
        print_colored("Ошибка: Файл layer11.py не найден", "red")
        return
    
    if not os.path.exists("deobfuscate_layer11.py"):
        print_colored("Ошибка: Файл deobfuscate_layer11.py не найден", "red")
        return
    
    # Анализируем файл layer11.py
    print_colored("Анализ файла layer11.py", "blue")
    analyze_layer11_file()
    
    # Запускаем деобфускацию
    print_colored("\nЗапуск процесса деобфускации", "blue")
    success, output = run_command(
        [sys.executable, "deobfuscate_layer11.py"],
        "Запуск деобфускатора слоя 11"
    )
    
    if not success:
        print_colored("Процесс деобфускации завершился с ошибкой", "red")
        return
    
    # Проверяем результат
    if os.path.exists("layer12.py"):
        # Подсчитываем статистику
        layer11_size = os.path.getsize("layer11.py")
        layer12_size = os.path.getsize("layer12.py")
        
        print_colored("\nСтатистика результатов:", "green")
        print(f"- Размер слоя 11: {layer11_size} байт")
        print(f"- Размер слоя 12: {layer12_size} байт")
        print(f"- Разница: {layer12_size - layer11_size:+d} байт ({(layer12_size / layer11_size * 100):.1f}%)")
        
        # Анализируем улучшения
        with open("layer11.py", 'r', encoding='utf-8') as f:
            content11 = f.read()
        
        with open("layer12.py", 'r', encoding='utf-8') as f:
            content12 = f.read()
        
        # Подсчитываем количество переменных var_X до и после
        var_pattern = r'var_\d+'
        var_matches11 = re.findall(var_pattern, content11)
        var_matches12 = re.findall(var_pattern, content12)
        
        print(f"- Переменные var_X: {len(var_matches11)} → {len(var_matches12)} ({len(var_matches12) - len(var_matches11):+d})")
        
        # Подсчитываем количество байтовых строк до и после
        bytes_pattern = r'b[\'"]([^\'"]*)[\'"]'
        bytes_matches11 = re.findall(bytes_pattern, content11)
        bytes_matches12 = re.findall(bytes_pattern, content12)
        
        print(f"- Байтовые строки: {len(bytes_matches11)} → {len(bytes_matches12)} ({len(bytes_matches12) - len(bytes_matches11):+d})")
        
        # Подсчитываем количество вызовов getattr до и после
        getattr_pattern = r'getattr\([^,]+,\s*([^,)]+)'
        getattr_matches11 = re.findall(getattr_pattern, content11)
        getattr_matches12 = re.findall(getattr_pattern, content12)
        
        print(f"- Вызовы getattr(): {len(getattr_matches11)} → {len(getattr_matches12)} ({len(getattr_matches12) - len(getattr_matches11):+d})")
        
        # Подсчитываем количество вызовов xor_decode до и после
        xor_decode_pattern = r'xor_decode\(([^)]+)\)'
        xor_decode_matches11 = re.findall(xor_decode_pattern, content11)
        xor_decode_matches12 = re.findall(xor_decode_pattern, content12)
        
        print(f"- Вызовы xor_decode(): {len(xor_decode_matches11)} → {len(xor_decode_matches12)} ({len(xor_decode_matches12) - len(xor_decode_matches11):+d})")
        
        # Подсчитываем количество вызовов unknown_1 до и после
        unknown_pattern = r'unknown_1\(([^)]+)\)'
        unknown_matches11 = re.findall(unknown_pattern, content11)
        unknown_matches12 = re.findall(unknown_pattern, content12)
        
        print(f"- Вызовы unknown_1(): {len(unknown_matches11)} → {len(unknown_matches12)} ({len(unknown_matches12) - len(unknown_matches11):+d})")
        
        print_colored("\nДеобфускация успешно завершена!", "green")
        print_colored(f"Результат сохранен в файл: layer12.py", "green")
        print_colored("Для продолжения деобфускации используйте файл layer12.py", "green")
    else:
        print_colored("Ошибка: Файл layer12.py не был создан", "red")

if __name__ == "__main__":
    main() 