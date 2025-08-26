"""
Деобфусцированная версия файла layer10.py
Телеграм-бот с веб-сервером на основе aiogram и aiohttp.
"""

def decode(obj, *a, **kw):
    """Декодирует байтовые объекты в строки, используя кодировку utf-8 по умолчанию."""
    if isinstance(obj, (bytes, bytearray)):
        return obj.decode(*(a or ('utf-8',)), **kw)
    return obj


"""
Однострочный декодер (и одновременно кодер) для строк,
зашифрованных функцией `xor_transform` из obf‑скрипта.

Использование
-------------
>>> from xor_transform import decrypt, encrypt
>>> raw = b"Hello, world!"
>>> enc = encrypt(raw)          # шифруем
>>> dec = decrypt(enc)          # обратно
>>> dec == raw                  # True
"""
from typing import ByteString, Union
import importlib, builtins, types, sys, os, signal, asyncio, logging

# Ключ для XOR-шифрования
KEY: bytes = bytes.fromhex(
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


encrypt = xor_transform
decrypt = xor_transform
__all__ = ['KEY', 'xor_transform', 'encrypt', 'decrypt']


def patches(mod, *args, **kw):
    """Загружает модуль по имени."""
    return importlib.import_module(mod)


async def _dummy(*a, **kw):
    """Пустая асинхронная функция."""
    pass


# Импорт основных модулей
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# Настройки приложения
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", "")  # Токен API Telegram
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "127.0.0.1")  # Хост для вебхука
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))  # Порт для вебхука
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")  # Путь для вебхука
API_PATH = os.getenv("API_PATH", "/api/")  # Базовый путь API
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")  # Хост сервера
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))  # Порт сервера
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "0"))  # Интервал опроса
SCHEDULED_TASKS = int(os.getenv("SCHEDULED_TASKS", "0"))  # Количество запланированных задач
WEBHOOK_MODE = os.getenv("WEBHOOK_MODE", "0").lower() in ("1", "true", "yes")  # Режим вебхука
USE_STATICS = os.getenv("USE_STATICS", "0").lower() in ("1", "true", "yes")  # Использовать статические файлы
USE_TEMPLATES = os.getenv("USE_TEMPLATES", "0").lower() in ("1", "true", "yes")  # Использовать шаблоны
ENABLE_API = os.getenv("ENABLE_API", "0").lower() in ("1", "true", "yes")  # Включить API
ENABLE_DOCS = os.getenv("ENABLE_DOCS", "0").lower() in ("1", "true", "yes")  # Включить документацию
ENABLE_USERS = os.getenv("ENABLE_USERS", "0").lower() in ("1", "true", "yes")  # Включить пользователей
STATIC_FILES_PATH = os.getenv("STATIC_FILES_PATH", "static")  # Путь к статическим файлам
CURRENT_VERSION = "5.131"  # Текущая версия API

# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# URL вебхука
webhook_url = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Обработчики маршрутов
async def get_token():
    """Получение токена API."""
    # В реальном приложении здесь может быть логика получения токена из БД или другого источника
    return API_TOKEN


async def process_updates(bot):
    """Обработка обновлений от Telegram."""
    # Логика обработки сообщений от Telegram
    pass


async def scheduler():
    """Планировщик задач."""
    # Логика планирования и выполнения задач
    pass


async def api_handler(request):
    """Обработчик API запросов."""
    return web.json_response({"status": "ok", "version": CURRENT_VERSION})


async def template_handler(request):
    """Обработчик запросов к шаблонам."""
    return web.Response(text="Templates handler")


async def docs_handler(request):
    """Обработчик запросов к документации."""
    return web.Response(text="Documentation")


async def user_handler(request):
    """Обработчик запросов к пользователям."""
    email = request.match_info.get("email", "")
    return web.json_response({"email": email})


async def message_handler(request):
    """Обработчик сообщений."""
    email = request.match_info.get("email", "")
    tg_id = request.match_info.get("tg_id", "")
    return web.json_response({"email": email, "tg_id": tg_id})


# Функция для установки утилиты solobot
def install_solobot():
    """Установка команды solobot для быстрого запуска приложения."""
    script_path = os.path.abspath(__file__)
    python_executable = sys.executable
    
    # Пути для установки команды
    bin_paths = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/bin')]
    
    # Ищем доступный путь для установки
    for bin_path in bin_paths:
        if os.path.exists(bin_path) and os.access(bin_path, os.W_OK):
            solobot_path = os.path.join(bin_path, 'solobot')
            break
    else:
        print("❌ Не удалось найти подходящую директорию для установки утилиты.")
        return
    
    # Если файл уже существует, пропускаем установку
    if os.path.exists(solobot_path):
        return
    
    try:
        # Создаем исполняемый файл
        with open(solobot_path, 'w') as f:
            f.write(f"""#!/bin/bash
'{python_executable}' '{script_path}' "$@"
""")
        
        # Даем файлу права на исполнение (0o755)
        os.chmod(solobot_path, 493)  # 493 = 0o755
        
        print("✅ Команда solobot установлена и теперь доступна. Используйте: solobot")
    except Exception as e:
        print(f'❌ Ошибка установки команды solobot: {e}')


# Функция периодической задачи
async def periodic_task():
    """Выполняет задачу периодически с заданным интервалом."""
    while True:
        await asyncio.sleep(5)  # Ожидаем указанное время
        await asyncio.sleep(POLL_INTERVAL)  # Используем интервал из настроек


# Функция запуска при старте приложения
async def on_startup(app):
    """Выполняется при запуске приложения."""
    # Настраиваем вебхук для бота
    await bot.set_webhook(webhook_url)
    await dp.start_polling()  # Запускаем опрос обновлений
    
    # Запускаем основную задачу для обработки сообщений
    asyncio.create_task(process_updates(bot))
    
    # Запускаем периодические задачи если включены
    if POLL_INTERVAL > 0:
        asyncio.create_task(periodic_task())
    if SCHEDULED_TASKS > 0:
        asyncio.create_task(scheduler())


# Функция завершения при остановке приложения
async def on_shutdown(app):
    """Выполняется при завершении работы приложения."""
    # Закрываем соединения и очищаем ресурсы
    await bot.close()
    
    # Отменяем все задачи
    for task in asyncio.all_tasks():
        task.cancel()
    
    # Ждем завершения всех задач
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=True)
    except Exception as e:
        logging.error(f'Ошибка при завершении работы: {e}')


# Обработчик для остановки сервера
async def handle_stop(site):
    """Обрабатывает сигнал остановки сервера."""
    logging.info("Получен сигнал остановки, завершаем работу...")
    await site.stop()
    logging.info("Сервер остановлен")


# Основная функция запуска приложения
async def main():
    """Основная функция запуска веб-сервера и бота."""
    # Проверка токена
    token = await get_token()
    if not token:
        logging.error("Не удалось получить токен API. Проверьте настройки и повторите попытку.")
        return
    
    # Проверка версии API
    api_version = "5.131"  # Версия API
    if CURRENT_VERSION != api_version:
        logging.error("Неподдерживаемая версия API. Обновите приложение.")
        return
    
    # Инициализация диспетчера
    dp.start_polling()
    
    if WEBHOOK_MODE:
        # Запуск в режиме вебхука (для продакшена)
        logging.info("Запуск в режиме вебхука")
        
        # Инициализация бота и диспетчера
        await bot.initialize()
        await dp.start_polling()
        
        # Создаем задачи
        tasks = [asyncio.create_task(process_updates(bot))]
        
        # Добавляем периодические задачи если нужно
        if SCHEDULED_TASKS > 0:
            tasks.append(asyncio.create_task(scheduler()))
        if POLL_INTERVAL > 0:
            tasks.append(asyncio.create_task(periodic_task()))
        
        # Настраиваем обработку обновлений
        await dp.start_polling(bot)
        
        logging.info("Обработчик обновлений запущен, ожидаем сообщения")
        
        # Ждем завершения всех задач
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    else:
        # Запуск в режиме длительного опроса (для разработки)
        logging.info("Запуск в режиме сервера")
        
        # Создаем экземпляр приложения
        app = web.Application()
        
        # Регистрируем обработчики
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        
        # Добавляем маршруты
        if USE_STATICS:
            app.router.add_static("/static", STATIC_FILES_PATH)
        if USE_TEMPLATES:
            app.router.add_get("/templates", template_handler)
        if ENABLE_API:
            app.router.add_get("/api", api_handler)
        if ENABLE_DOCS:
            app.router.add_get("/docs", docs_handler)
        if ENABLE_USERS:
            app.router.add_get(f"{API_PATH}{{email}}", user_handler)
        
        # Маршрут для обработки вебхуков
        app.router.add_get(f"{API_PATH}{{email}}/{{tg_id}}", message_handler)
        
        # Настраиваем обработчик для телеграм-бота
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
        
        # Дополнительная настройка приложения
        setup_application(app, dp, bot=bot)
        
        # Запускаем сервер
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=SERVER_HOST, port=SERVER_PORT)
        await site.start()
        
        # Выводим информацию о запуске
        logging.info(f'URL вебхука: {webhook_url}')
        
        # Обработка сигналов остановки
        stop_event = asyncio.Event()
        loop = asyncio.get_event_loop()
        
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        
        try:
            # Ожидаем сигнала остановки
            await stop_event.wait()
        finally:
            # Останавливаем все задачи
            pending_tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            for task in pending_tasks:
                try:
                    task.cancel()
                except Exception as e:
                    logging.error(e)
            
            # Ждем завершения задач
            await asyncio.gather(*pending_tasks, return_exceptions=True)


# Запуск приложения при прямом вызове скрипта
if __name__ == '__main__':
    install_solobot()
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"""Ошибка при запуске приложения:
{e}""") 