#!/usr/bin/env python3

import os
import subprocess
import sys
import time

def print_header(text, char="="):
    """Печатает заголовок с рамкой"""
    width = 70
    print(char * width)
    print(text.center(width))
    print(char * width)
    print()

def print_step(step_num, description):
    """Печатает информацию о текущем шаге"""
    print(f"Шаг {step_num}: {description}")
    print("-" * 50)

def run_command(command, description=None):
    """Запускает команду и печатает вывод"""
    if description:
        print(f"{description}...")
    
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Вывод команды:")
        print(result.stdout)
        
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print("Вывод команды:")
        print(e.stdout)
        print("Ошибки:")
        print(e.stderr)
        return False

def main():
    input_file = "layer7.py"
    output_file = "layer8.py"
    temp_file_1 = "layer7_decoded.py"
    
    print_header("ПРОЦЕСС ДЕОБФУСКАЦИИ СЛОЯ 7")
    
    # Проверка наличия всех необходимых файлов
    required_files = [
        "layer7.py",
        "deobfuscate_layer7.py",
        "u1KQ2EguJKQ7_analyzer.py",
        "decode_strings.py"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Ошибка: Файл {file} не найден")
            return
    
    print("Все необходимые файлы найдены.")
    print()
    
    # Шаг 1: Анализ функции u1KQ2EguJKQ7
    print_step(1, "Анализ функции декодирования u1KQ2EguJKQ7")
    
    if not run_command(
        [sys.executable, "u1KQ2EguJKQ7_analyzer.py", input_file],
        "Запуск анализатора функции u1KQ2EguJKQ7"
    ):
        print("Не удалось проанализировать функцию декодирования")
        return
    
    # Проверяем наличие файла decode_xor.py
    if not os.path.exists("decode_xor.py"):
        print("Ошибка: Не найден файл decode_xor.py с функцией декодирования")
        return
    
    print("Анализ функции u1KQ2EguJKQ7 завершен.")
    print()
    
    # Шаг 2: Декодирование зашифрованных строк
    print_step(2, "Декодирование зашифрованных строк")
    
    if not run_command(
        [sys.executable, "decode_strings.py", input_file, "decode_xor.py", temp_file_1],
        "Запуск декодирования строк"
    ):
        print("Не удалось декодировать зашифрованные строки")
        return
    
    print("Декодирование строк завершено.")
    print()
    
    # Шаг 3: Применение деобфускатора
    print_step(3, "Применение основного деобфускатора")
    
    if not run_command(
        [sys.executable, "deobfuscate_layer7.py"],
        "Запуск основного деобфускатора"
    ):
        print("Не удалось применить основной деобфускатор")
        return
    
    print("Применение деобфускатора завершено.")
    print()
    
    # Завершение
    print_header("ДЕОБФУСКАЦИЯ ЗАВЕРШЕНА", "*")
    
    print(f"Деобфусцированный код сохранен в файл: {output_file}")
    print()
    print("Промежуточные файлы:")
    print(f"- {temp_file_1} - файл с декодированными строками")
    print(f"- decode_xor.py - модуль с функцией декодирования")
    print()
    
    # Статистика результатов
    if os.path.exists(output_file):
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        
        print("Статистика:")
        print(f"- Размер исходного файла: {input_size} байт")
        print(f"- Размер деобфусцированного файла: {output_size} байт")
        print(f"- Разница: {output_size - input_size} байт ({(output_size / input_size * 100):.1f}%)")
    
    print()
    print("Для продолжения деобфускации следующего слоя используйте файл layer8.py")

if __name__ == "__main__":
    main() 