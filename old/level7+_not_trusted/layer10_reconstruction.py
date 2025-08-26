#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Телеграм бот с веб-сервером для обработки вебхуков.
Этот код был восстановлен из обфусцированного файла layer10.py.
"""

import os
import sys
import asyncio
import signal
from typing import ByteString, Union
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook import configure_app, SimpleRequestHandler

# Константы и настройки
API_TOKEN = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"  # Замените на свой токен
WEBHOOK_HOST = "example.com"  # Замените на хост вашего сервера
WEBHOOK_PORT = 8443  # Или 80, 88, 443
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

EMAIL_PATH_PREFIX = "/email/"  # Префикс для обработки email-запросов

# Настройки режима работы
USE_WEBHOOK = True  # Использовать webhook или поллинг
USE_POST = True  # Обрабатывать POST запросы
USE_GET = True  # Обрабатывать GET запросы
USE_EMAIL_HANDLER = True  # Обрабатывать запросы по email
USE_GET_HANDLER = True  # Использовать обработчик GET запросов
USE_POST_HANDLER = True  # Использовать обработчик POST запросов

POLL_INTERVAL = 5  # Интервал поллинга в секундах (если не используется webhook)
POLL_TIMEOUT = 30  # Таймаут поллинга в секундах

# Ключ для XOR-шифрования
KEY = bytes.fromhex(
    '3c104b151941360c2b11031e13180f3d0b0b041619132e070d15070a0c00031e18071d0f1a0a'
)

def xor_transform(data: ByteString, key: bytes=KEY) -> bytes:
    """
    Универсальная функция XOR‑преобразования.
    Для исходного алгоритма ENCRYPT == DECRYPT.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError('data must be bytes‑like object')
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

# Определяем функции шифрования/дешифрования
encrypt = xor_transform
decrypt = xor_transform

def setup_solobot():
    """
    Создает команду solobot в системе для быстрого запуска бота.
    """
    script_path = os.path.abspath(__file__)
    python_path = sys.executable
    paths = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    
    for folder in paths:
        if os.path.isdir(folder) and os.access(folder, os.X_OK):
            bot_path = os.path.join(folder, 'solobot')
            break
    else:
        print("❌ Ошибка: Не удалось найти подходящую директорию для команды solobot.")
        return
    
    if os.path.exists(bot_path):
        return
    
    try:
        with open(bot_path, 'w') as file:
            file.write(f"""#!/bin/bash
'{python_path}' '{script_path}' "$@"
""")
        os.chmod(bot_path, 0o755)
        print(f"✅ Команда `solobot` установлена! Используйте: solobot")
    except Exception as err:
        print(f'❌ Ошибка установки команды solobot: {err}')

async def polling_task(bot, interval=POLL_INTERVAL):
    """
    Функция периодического опроса сервера Telegram API.
    """
    while True:
        await asyncio.sleep(interval)
        # Здесь может быть дополнительный код для обработки обновлений

async def check_token():
    """
    Проверяет валидность токена API.
    """
    try:
        # Здесь должен быть код проверки токена
        return True
    except Exception:
        return False

async def on_startup(app):
    """
    Инициализация при запуске.
    """
    bot = app['bot']
    
    # Устанавливаем вебхук
    await bot.set_webhook(WEBHOOK_URL)
    
    # Дополнительные инициализации можно добавить здесь
    
    if POLL_INTERVAL > 0:
        asyncio.create_task(polling_task(bot, POLL_INTERVAL))

async def on_shutdown(app):
    """
    Завершение работы приложения.
    """
    bot = app['bot']
    
    # Удаляем вебхук при завершении работы
    await bot.delete_webhook()
    
    # Отменяем все задачи
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()
    
    try:
        # Ждем завершения всех задач
        pending = asyncio.all_tasks()
        await asyncio.gather(*pending, return_exceptions=True)
    except Exception as err:
        print(f'Ошибка при завершении работы: {err}')

async def stop_server(site):
    """
    Останавливает веб-сервер.
    """
    print("Начинаю остановку веб-сервера...")
    await site.stop()
    print("Веб-сервер остановлен")

async def handle_email(request):
    """
    Обработчик для email-запросов.
    """
    email = request.match_info.get('email', '')
    return web.json_response({"status": "ok", "email": email})

async def handle_email_tg(request):
    """
    Обработчик для email-запросов с привязкой к Telegram ID.
    """
    email = request.match_info.get('email', '')
    tg_id = request.match_info.get('tg_id', '')
    return web.json_response({"status": "ok", "email": email, "tg_id": tg_id})

async def get_handler(request):
    """
    Обработчик GET-запросов.
    """
    return web.json_response({"status": "ok", "method": "GET"})

async def post_handler(request):
    """
    Обработчик POST-запросов.
    """
    return web.json_response({"status": "ok", "method": "POST"})

async def main():
    """
    Основная функция запуска бота.
    """
    # Проверяем токен API
    token_valid = await check_token()
    if not token_valid:
        print("❌ Ошибка: Не удалось проверить API токен. Проверьте доступность API и сетевое подключение.")
        return
    
    # Создаем экземпляры бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dispatcher = Dispatcher(bot)
    
    if USE_WEBHOOK:
        print("✅ Запуск бота в режиме webhook")
        
        # Инициализация бота
        await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL)
        
        # Создаем и настраиваем веб-приложение
        app = web.Application()
        app['bot'] = bot
        
        # Устанавливаем обработчики событий
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        
        # Настраиваем вебхук для aiogram
        SimpleRequestHandler(
            dispatcher=dispatcher,
            bot=bot,
        ).register(app, path=WEBHOOK_PATH)
        
        # Регистрируем дополнительные обработчики маршрутов
        if USE_GET_HANDLER:
            app.router.add_get('/get', get_handler)
        if USE_POST_HANDLER:
            app.router.add_post('/post', post_handler)
        if USE_EMAIL_HANDLER:
            app.router.add_get(f'{EMAIL_PATH_PREFIX}{{email}}', handle_email)
            app.router.add_get(f'{EMAIL_PATH_PREFIX}{{email}}/{{tg_id}}', handle_email_tg)
        
        # Запускаем веб-сервер
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=WEBHOOK_HOST, port=WEBHOOK_PORT)
        await site.start()
        
        print(f"✅ Webhook настроен успешно. URL: {WEBHOOK_URL}")
        
        # Ожидаем сигнала для завершения
        stop_event = asyncio.Event()
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        
        try:
            await stop_event.wait()
        finally:
            # Останавливаем веб-сервер при завершении
            await site.stop()
            await runner.cleanup()
    else:
        print("✅ Запуск бота в режиме поллинга")
        # В режиме поллинга используем start_polling
        try:
            await dispatcher.start_polling(bot, poll_interval=POLL_INTERVAL)
        finally:
            await bot.session.close()

if __name__ == '__main__':
    setup_solobot()
    try:
        asyncio.run(main())
    except Exception as err:
        print(f"""Ошибка при запуске приложения:
{err}""") 