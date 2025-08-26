def xor_decode(data):
    # Декодирует данные, используя XOR-шифрование с ключом
    # Ключ XOR
    key = [
        52, 110, 103, 144, 44, 41, 159, 75, 3, 6, 
        103, 45, 15, 232, 5, 168, 186, 101, 136, 199, 
        76, 59, 74, 28, 139, 166, 10, 120, 93, 139, 
        58, 48, 248, 136, 234, 128, 174, 58, 109, 129
    ]
    
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def import_module(var_1, var_2, *var_3, **var_4):
    try:
        return __import__(
            var_1 + "." + var_2,
            *var_3,
            **var_4,
        )
    except Exception:
        return __import__(var_1, *var_3, **var_4)

import asyncio
import signal
import aiohttp
import os
import logging as logger

# Определение глобальных переменных

register_webapps = None

webapps_manager = None

bot = None

dp = None

periodic_task_interval = 60  # Значение по умолчанию

handle_commands = True

use_webhook = False

use_custom_templates = False

process_metrics = False

base_url = '/'

host = '0.0.0.0'

port = 8080

bot_path = ''

webhook_url = ''

handle_oauth = False

handle_auth = False

check_interval = 0

var_27 = None  # Обработчик сообщений

var_28 = None  # Обработчик веб-маршрутов

var_30 = None  # Неизвестная функция

command_handler = None

scheduler_task = None

scheduler_task_2 = None

scheduler_task_3 = None

metrics_handler = None

var_34 = None  # Токен или другая настройка

oauth_handler = None

auth_handler = None



def install_solobot():
    script_path = os.path.abspath("solobot.py")
    python_path = "python3"  # Предполагаемый путь к Python
    
    # Список потенциальных директорий для установки
    bin_dirs = [
        "/usr/local/bin",
        "/usr/bin",
        os.path.expanduser("~/.local/bin")
    ]
    
    # Поиск доступной директории
    for bin_dir in bin_dirs:
        if os.path.exists(bin_dir) and os.access(bin_dir, os.W_OK):
            cmd_path = os.path.join(bin_dir, "solobot")
            break
    else:
        print("Не удалось найти подходящую директорию для установки команды solobot.")
        return
    
    # Если файл уже существует, не перезаписываем
    if os.path.exists(cmd_path):
        return
    
    try:
        with open(cmd_path, "w") as f:
            f.write(f'#!/bin/bash\n{python_path} {script_path} "$@"\n')
        
        os.chmod(cmd_path, 0o755)  # Делаем файл исполняемым
        print("✅ Команда `solobot` установлена! Используйте: solobot")
    except Exception as e:
        print(f"❌ Ошибка установки команды solobot: {e}")

async def periodic_task():
    while True:
        await scheduler_task()
        await asyncio.sleep(periodic_task_interval)

async def on_startup(app):
    await bot.set_webhook(webhook_url)
    await scheduler_task_2()
    
    if periodic_task_interval > 0:
        asyncio.create_task(periodic_task())
    
    if check_interval > 0:
        asyncio.create_task(periodic_task())

async def on_shutdown(app):
    await bot.delete_webhook()
    
    for task in asyncio.all_tasks():
        task.cancel()
    
    try:
        await asyncio.gather(
            *asyncio.all_tasks(),
            return_exceptions=True
        )
    except Exception as e:
        logger.error(f"Ошибка при завершении работы: {e}")

async def handle_stop(site):
    logger.info("Останавливаю сервер...")
    await site.stop()
    logger.info("Сервер остановлен.")

async def main():
    result = await scheduler_task_3()
    if not result:
        logger.error("Не удалось выполнить начальную проверку. Завершение работы.")
        return
    
    expected_token = "YOUR_EXPECTED_TOKEN"  # Предполагаемый токен
    if var_34 != expected_token:
        logger.error("Неверный токен. Завершение работы.")
        return
    
    dp.register_message_handler(var_27)
    
    if use_webhook:
        logger.info("Запуск в режиме вебхука")
        await bot.delete_webhook()
        await scheduler_task_2()
        
        tasks = [asyncio.create_task(var_30(bot))]
        
        if check_interval > 0:
            tasks.append(
                asyncio.create_task(periodic_task())
            )
        
        if periodic_task_interval > 0:
            tasks.append(
                asyncio.create_task(periodic_task())
            )
        
        await dp.start_polling(bot)
        
        logger.info("Бот запущен. Для остановки нажмите Ctrl+C")
        
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )
    else:
        logger.info("Запуск в режиме приложения")
        
        app = aiohttp.web.Application()
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        
        if handle_oauth:
            app.router.add_route("GET", "/oauth", oauth_handler)
        
        if handle_auth:
            app.router.add_route("GET", "/auth", auth_handler)
        
        if handle_commands:
            app.router.add_route("POST", "/commands", command_handler)
        
        if process_metrics:
            app.router.add_route("GET", "/metrics", metrics_handler)
        
        if use_custom_templates:
            app.router.add_get(f"{base_url}{{email}}", handle_template)
            app.router.add_get(f"{base_url}{{email}}/{{tg_id}}", var_28)
        
        # Настройка веб-приложений
        register_webapps(dp=dp, bot=bot)
        webapps_manager(app, dp, bot=bot)
        
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        
        site = aiohttp.web.TCPSite(
            runner, host=host, port=port
        )
        
        await site.start()
        logger.info(f"URL вебхука: {webhook_url}")
        
        # Настройка обработки сигналов
        event = asyncio.Event()
        signal_handler = lambda s: event.set()
        
        for sig in (
            signal.SIGINT,
            signal.SIGTERM,
        ):
            signal.signal(sig, signal_handler)
            
        try:
            await event.wait()
        finally:
            tasks_to_cancel = [
                task
                for task in asyncio.all_tasks()
                if task is not asyncio.current_task()
            ]
            
            for task in tasks_to_cancel:
                try:
                    task.cancel()
                except Exception as e:
                    logger.error(e)
            
            await asyncio.gather(
                *tasks_to_cancel,
                return_exceptions=True
            )

if __name__ == "__main__":
    install_solobot()
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения:\n{e}")
