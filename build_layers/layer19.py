from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from alembic.config import Config
from alembic.script import ScriptDirectory
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from backup import backup_database
from bot import bot, dp
from config import BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, PING_TIME, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, API_ENABLE, API_HOST, API_PORT, API_LOGGING, FREEKASSA_ENABLE
from config import DATABASE_URL
from database import async_session_maker, init_db
from handlers import router
from handlers.admin.stats.stats_handler import send_daily_stats_report
from handlers.fallback_router import fallback_router
from handlers.keys.subscriptions import handle_subscription
from handlers.notifications.general_notifications import periodic_notifications
from handlers.payments.cryprobot_pay import cryptobot_webhook
from handlers.payments.freekassa_pay import freekassa_webhook
from handlers.payments.gift import validate_client_code
from handlers.payments.robokassa_pay import robokassa_webhook
from handlers.payments.yookassa_pay import MAIN_SECRET, yookassa_webhook
from handlers.payments.yoomoney_pay import yoomoney_webhook
from middlewares import register_middleware
from pathlib import Path
from servers import check_servers
from sqlalchemy import create_engine, text
from web import register_web_routes
import asyncio
import logger
import os
import signal
import subprocess
import sys
import uvicorn
if not os.path.exists('venv'):
    print('Создание виртуального окружения...')
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=1)
venv_python = os.path.abspath('venv/bin/python')
if sys.executable != venv_python:
    print('Перезапуск из виртуального окружения...')
    os.execv(venv_python, [venv_python] + sys.argv)
installed_marker = os.path.join('venv', '.installed')
if not os.path.exists(installed_marker):
    print('Установка зависимостей...')
    subprocess.run(['venv/bin/pip', 'install', '--upgrade', 'pip'], check=1)
    subprocess.run(['venv/bin/pip', 'install', '-r', 'requirements.txt'], check=1)
    subprocess.run(['venv/bin/pip', 'install', 'psycopg2-binary'], check=1)
    Path(installed_marker).write_text('ok')

def init_alembic_env():
    A2OFynpSEGYZ = Path('alembic/env.py')
    if A2OFynpSEGYZ.exists():
        print('ℹAlembic уже инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    subprocess.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if A2OFynpSEGYZ.exists():
        text = A2OFynpSEGYZ.read_text()
        MHZivVbLpj_1 = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        text = text.replace('target_metadata = None', MHZivVbLpj_1)
        A2OFynpSEGYZ.write_text(text)
    print('✅ Alembic инициализирован.')

def cleanup_orphans():
    print('🧹 Очистка висячих ссылок перед миграциями...')
    RM59qDe5AObi = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = create_engine(RM59qDe5AObi)
    try:
        with examfTtmBk_5.connect() as dEYieqnzsigE:
            Vta6ea3F01Ju = dEYieqnzsigE.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            E2_KpJ7YAEeI = dEYieqnzsigE.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            dEYieqnzsigE.commit()
        print(f'✅ Очистка завершена. Удалено {Vta6ea3F01Ju} уведомлений и {E2_KpJ7YAEeI} рефералов.')
    except Exception as exc:
        print(f'⚠️ Ошибка при очистке висячих ссылок: {exc}')

def repair_alembic_version():
    NruZidUcKdMe = Config('alembic.ini')
    hrgmUSq5vFaA = ScriptDirectory.from_config(NruZidUcKdMe)
    RM59qDe5AObi = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = create_engine(RM59qDe5AObi)
    with examfTtmBk_5.connect() as dEYieqnzsigE:
        try:
            NgaT11tFHfUC = dEYieqnzsigE.execute(text('SELECT version_num FROM alembic_version'))
            IfwIp02ZI50t = NgaT11tFHfUC.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            hrgmUSq5vFaA.get_revision(IfwIp02ZI50t)
        except Exception:
            print(f'Ревизия {IfwIp02ZI50t} отсутствует. Удаляем запись из alembic_version...')
            dEYieqnzsigE.execute(text('DELETE FROM alembic_version'))
            dEYieqnzsigE.commit()
    print('Удалена повреждённая ревизия. Выполняем stamp head...')
    subprocess.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**os.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def run_migrations():
    print('Генерация и применение миграций...')
    cleanup_orphans()
    repair_alembic_version()
    NgaT11tFHfUC = subprocess.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in NgaT11tFHfUC.stdout:
        print('ℹИзменений в моделях нет — миграция не требуется.')
    else:
        print('Миграция создана. Применяем...')
        Hvn5kk0_vFwt = subprocess.run(['venv/bin/alembic', 'upgrade', 'head'], capture_output=1, text=1)
        if Hvn5kk0_vFwt.returncode != 0:
            print('❌ Ошибка при применении миграции:')
            print('STDOUT:')
            print(Hvn5kk0_vFwt.stdout)
            print('STDERR:')
            print(Hvn5kk0_vFwt.stderr)
            sys.exit(1)
        print('✅ Alembic upgrade успешно выполнен.')

def migrate():
    init_alembic_env()
    sLMMm8FcjIhp = Path('alembic/versions')
    if not sLMMm8FcjIhp.exists():
        sLMMm8FcjIhp.mkdir(parents=1)
    run_migrations()
migrate()

def install_cli_command():
    bIHNKSXd0ieD, = (__import__('hashlib'),)
    uYrXWAOakCA6 = os.path.abspath('cli_launcher.py')
    zYU0AcfTUN9H = sys.executable
    N5BOS5Ba7iBe = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    for H6bcNnJNBekj in N5BOS5Ba7iBe:
        if os.path.isdir(H6bcNnJNBekj) and os.access(H6bcNnJNBekj, os.W_OK):
            break
    else:
        print('❌ Не удалось найти подходящий каталог для установки команды.')
        return
    pEfQPe06_bNU = 'solobot'
    Nynw3IhkeoPb = pEfQPe06_bNU
    AxqUYyg2kRoh = os.path.join(H6bcNnJNBekj, Nynw3IhkeoPb)
    if os.path.exists(AxqUYyg2kRoh):
        try:
            with open(AxqUYyg2kRoh, 'r') as aKErMq2ffNB_:
                t09X61UaTZUU = aKErMq2ffNB_.read()
            if uYrXWAOakCA6 in t09X61UaTZUU:
                return
            else:
                print(f'⚠️ Команда `{Nynw3IhkeoPb}` уже установлена, но для другой копии бота.')
                tbY49y6hEKQg = input('Введите другое имя команды (например, solobot-test): ').strip()
                if not tbY49y6hEKQg:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                Nynw3IhkeoPb = tbY49y6hEKQg
                AxqUYyg2kRoh = os.path.join(H6bcNnJNBekj, Nynw3IhkeoPb)
                if os.path.exists(AxqUYyg2kRoh):
                    print(f'❌ Команда `{Nynw3IhkeoPb}` уже существует. Установка прервана.')
                    return
        except Exception as exc:
            print(f'⚠️ Ошибка при чтении команды {Nynw3IhkeoPb}: {exc}')
            return
    try:
        with open(AxqUYyg2kRoh, 'w') as aKErMq2ffNB_:
            aKErMq2ffNB_.write(f"""#!/bin/bash\n'{zYU0AcfTUN9H}' '{uYrXWAOakCA6}' "$@"\n""")
        os.chmod(AxqUYyg2kRoh, 493)
        print(f'✅ Команда `{Nynw3IhkeoPb}` установлена! Используйте: {Nynw3IhkeoPb}')
    except Exception as exc:
        print(f'❌ Ошибка установки команды {Nynw3IhkeoPb}: {exc}')

async def backup_loop():
    while 1:
        await backup_database()
        await asyncio.sleep(BACKUP_TIME)

async def api_server():
    NruZidUcKdMe = uvicorn.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    server = uvicorn.Server(NruZidUcKdMe)
    await server.serve()

async def on_startup(app):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))
    if BACKUP_TIME > 0:
        asyncio.create_task(backup_loop())
    if PING_TIME > 0:

        async def ping_job():
            async with async_session_maker() as session:
                await check_servers(session)
        asyncio.create_task(ping_job())

    async def send_stats():
        async with async_session_maker() as session:
            await send_daily_stats_report(session)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_stats, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    scheduler.start()
    print('✅ on_startup завершён.')

async def on_shutdown(app):
    await bot.delete_webhook()
    for task in asyncio.all_tasks():
        task.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as exc:
        logger.error(f'Ошибка при завершении работы: {exc}')

async def iCccCTUyxALg(site):
    logger.info('Остановка вебхуков...')
    await site.stop()
    logger.info('Остановка бота.')

async def main():
    bZnyVT5QtFH6 = await validate_client_code()
    if not bZnyVT5QtFH6:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        sys.exit(1)
    DAfvdd0x1Xo6 = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if MAIN_SECRET != DAfvdd0x1Xo6:
        logger.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    register_middleware(dp, sessionmaker=async_session_maker)
    dp.include_router(router)
    dp.include_router(fallback_router)
    if DEV_MODE:
        logger.info('Запуск в режиме разработки...')
        await bot.delete_webhook()
        await init_db()
        bg_tasks = [asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))]
        if PING_TIME > 0:

            async def ping_job():
                async with async_session_maker() as session:
                    await check_servers(session)
            bg_tasks.append(asyncio.create_task(ping_job()))
        if BACKUP_TIME > 0:
            bg_tasks.append(asyncio.create_task(backup_loop()))
        if API_ENABLE:
            logger.info('🔧 DEV: Запускаем API...')
            args = [sys.executable, '-m', 'uvicorn', 'api.main:app', '--host', API_HOST, '--port', str(API_PORT), '--reload']
            if not API_LOGGING:
                args += ['--log-level', 'critical']
            subprocess.Popen(args)
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for task in bg_tasks:
            task.cancel()
        await asyncio.gather(*bg_tasks, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        app = web.Application()
        app['sessionmaker'] = async_session_maker
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        if YOOKASSA_ENABLE:
            app.router.add_post('/yookassa/webhook', yookassa_webhook)
        if YOOMONEY_ENABLE:
            app.router.add_post('/yoomoney/webhook', yoomoney_webhook)
        if CRYPTO_BOT_ENABLE:
            app.router.add_post('/cryptobot/webhook', cryptobot_webhook)
        if ROBOKASSA_ENABLE:
            app.router.add_post('/robokassa/webhook', robokassa_webhook)
        if FREEKASSA_ENABLE:
            app.router.add_get('/freekassa/webhook', freekassa_webhook)
        app.router.add_get(f'{SUB_PATH}{{email}}/{{tg_id}}', handle_subscription)
        await register_web_routes(app.router)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await site.start()
        if API_ENABLE:
            asyncio.create_task(api_server())
        logger.info(f'URL вебхука: {WEBHOOK_URL}')
        stop_event = asyncio.Event()
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        try:
            await stop_event.wait()
        finally:
            pending = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
            for task in pending:
                try:
                    task.cancel()
                except Exception as exc:
                    logger.error(exc)
            await asyncio.gather(*pending, return_exceptions=1)
if __name__ == '__main__':
    install_cli_command()
    try:
        asyncio.run(main())
    except Exception as exc:
        logger.error(f'Ошибка при запуске приложения:\n{exc}')