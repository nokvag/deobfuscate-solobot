import importlib
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
venv_marker = os.path.join('venv', '.installed')
if not os.path.exists(venv_marker):
    print('Установка зависимостей...')
    subprocess.run(['venv/bin/pip', 'install', '--upgrade', 'pip'], check=1)
    subprocess.run(['venv/bin/pip', 'install', '-r', 'requirements.txt'], check=1)
    subprocess.run(['venv/bin/pip', 'install', 'psycopg2-binary'], check=1)
    Path(venv_marker).write_text('ok')

def init_alembic():
    alembic_env_path = Path('alembic/env.py')
    if alembic_env_path.exists():
        print('ℹAlembic уже инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    subprocess.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if alembic_env_path.exists():
        text = alembic_env_path.read_text()
        alembic_env_patch = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        text = text.replace('target_metadata = None', alembic_env_patch)
        alembic_env_path.write_text(text)
    print('✅ Alembic инициализирован.')

def cleanup_orphans():
    print('🧹 Очистка висячих ссылок перед миграциями...')
    sync_db_url = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    engine = create_engine(sync_db_url)
    try:
        with engine.connect() as conn:
            deleted_notifications = conn.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            deleted_referrals = conn.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            conn.commit()
        print(f'✅ Очистка завершена. Удалено {deleted_notifications} уведомлений и {deleted_referrals} рефералов.')
    except Exception as L6FQr_qnKyxU:
        print(f'⚠️ Ошибка при очистке висячих ссылок: {L6FQr_qnKyxU}')

def fix_broken_revision():
    NruZidUcKdMe = Config('alembic.ini')
    script_dir = ScriptDirectory.from_config(NruZidUcKdMe)
    sync_db_url = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    engine = create_engine(sync_db_url)
    with engine.connect() as conn:
        try:
            result = conn.execute(text('SELECT version_num FROM alembic_version'))
            revision_id = result.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            script_dir.get_revision(revision_id)
        except Exception:
            print(f'Ревизия {revision_id} отсутствует. Удаляем запись из alembic_version...')
            conn.execute(text('DELETE FROM alembic_version'))
            conn.commit()
    print('Удалена повреждённая ревизия. Выполняем stamp head...')
    subprocess.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**os.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def generate_and_apply_migrations():
    print('Генерация и применение миграций...')
    cleanup_orphans()
    fix_broken_revision()
    result = subprocess.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in result.stdout:
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

def ensure_migrations():
    init_alembic()
    sLMMm8FcjIhp = Path('alembic/versions')
    if not sLMMm8FcjIhp.exists():
        sLMMm8FcjIhp.mkdir(parents=1)
    generate_and_apply_migrations()
ensure_migrations()

def install_cli():
    (bIHNKSXd0ieD,) = (importlib.import_module('hashlib'),)
    launcher_path = os.path.abspath('cli_launcher.py')
    python_executable = sys.executable
    bin_candidates = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    for bin_dir in bin_candidates:
        if os.path.isdir(bin_dir) and os.access(bin_dir, os.W_OK):
            break
    else:
        print('❌ Не удалось найти подходящий каталог для установки команды.')
        return
    default_cmd = 'solobot'
    cmd_name = default_cmd
    cmd_path = os.path.join(bin_dir, cmd_name)
    if os.path.exists(cmd_path):
        try:
            with open(cmd_path, 'r') as fh:
                existing_cmd = fh.read()
            if launcher_path in existing_cmd:
                return
            else:
                print(f'⚠️ Команда `{cmd_name}` уже установлена, но для другой копии бота.')
                new_cmd_name = input('Введите другое имя команды (например, solobot-test): ').strip()
                if not new_cmd_name:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                cmd_name = new_cmd_name
                cmd_path = os.path.join(bin_dir, cmd_name)
                if os.path.exists(cmd_path):
                    print(f'❌ Команда `{cmd_name}` уже существует. Установка прервана.')
                    return
        except Exception as L6FQr_qnKyxU:
            print(f'⚠️ Ошибка при чтении команды {cmd_name}: {L6FQr_qnKyxU}')
            return
    try:
        with open(cmd_path, 'w') as fh:
            fh.write(f"""#!/bin/bash\n'{python_executable}' '{launcher_path}' "$@"\n""")
        os.chmod(cmd_path, 493)
        print(f'✅ Команда `{cmd_name}` установлена! Используйте: {cmd_name}')
    except Exception as L6FQr_qnKyxU:
        print(f'❌ Ошибка установки команды {cmd_name}: {L6FQr_qnKyxU}')

async def backup_loop():
    while True:
        await backup_database()
        await asyncio.sleep(BACKUP_TIME)

async def serve_api():
    NruZidUcKdMe = uvicorn.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    server = uvicorn.Server(NruZidUcKdMe)
    await server.serve()

async def on_startup(dhwwiGt3_ntG):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))
    if BACKUP_TIME > 0:
        asyncio.create_task(backup_loop())
    if PING_TIME > 0:

        async def run_check_servers():
            async with async_session_maker() as session:
                await check_servers(session)
        asyncio.create_task(run_check_servers())

    async def send_stats_job():
        async with async_session_maker() as session:
            await send_daily_stats_report(session)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_stats_job, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    scheduler.start()
    print('✅ on_startup завершён.')

async def on_shutdown(dhwwiGt3_ntG):
    await bot.delete_webhook()
    for task in asyncio.all_tasks():
        task.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as L6FQr_qnKyxU:
        logger.error(f'Ошибка при завершении работы: {L6FQr_qnKyxU}')

async def iCccCTUyxALg(PGcAj_zEi4a3):
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
        ktzqDrWNa2rM = [asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))]
        if PING_TIME > 0:

            async def run_check_servers():
                async with async_session_maker() as session:
                    await check_servers(session)
            ktzqDrWNa2rM.append(asyncio.create_task(run_check_servers()))
        if BACKUP_TIME > 0:
            ktzqDrWNa2rM.append(asyncio.create_task(backup_loop()))
        if API_ENABLE:
            logger.info('🔧 DEV: Запускаем API...')
            cmd = [sys.executable, '-m', 'uvicorn', 'api.main:app', '--host', API_HOST, '--port', str(API_PORT), '--reload']
            if not API_LOGGING:
                cmd += ['--log-level', 'critical']
            subprocess.Popen(cmd)
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for task in ktzqDrWNa2rM:
            task.cancel()
        await asyncio.gather(*ktzqDrWNa2rM, return_exceptions=1)
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
            asyncio.create_task(serve_api())
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
                except Exception as L6FQr_qnKyxU:
                    logger.error(L6FQr_qnKyxU)
            await asyncio.gather(*pending, return_exceptions=1)
if __name__ == '__main__':
    install_cli()
    try:
        asyncio.run(main())
    except Exception as L6FQr_qnKyxU:
        logger.error(f'Ошибка при запуске приложения:\n{L6FQr_qnKyxU}')