from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from alembic.config import Config
from alembic.script import ScriptDirectory
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot import bot, dp
from config import BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, PING_TIME, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, API_ENABLE, API_HOST, API_PORT, API_LOGGING, FREEKASSA_ENABLE, TRIBUTE_ENABLE
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
from handlers.payments.tribute_pay import tribute_webhook
from handlers.payments.yookassa_pay import MAIN_SECRET, yookassa_webhook
from handlers.payments.yoomoney_pay import yoomoney_webhook
from hooks.hooks import run_hooks
from middlewares import register_middleware
from pathlib import Path
from rich.console import Console
from servers import check_servers
from sqlalchemy import create_engine, text
from urllib.request import request
from web import register_web_routes
import asyncio
import logger
import os
import shutil
import signal
import subprocess
import sys
import uvicorn
import importlib
venv = Path('venv')
python = str(venv / 'bin' / 'python')
pip = str(venv / 'bin' / 'pip')
_installed = venv / '.installed'

def z8cSqgZUDjUT(TqUMzaW5W9NS, **afoXljZGRjuW):
    return subprocess.run(TqUMzaW5W9NS, check=1, **afoXljZGRjuW)
if not venv.exists():
    print('Создание виртуального окружения...')
    z8cSqgZUDjUT([sys.executable, '-m', 'venv', str(venv)])
try:
    z8cSqgZUDjUT([python, '-m', 'ensurepip', '--upgrade'])
except Exception:
    print('ensurepip недоступен, качаю get-pip.py…')
    get_pip_py = venv / 'get-pip.py'
    with request.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=30) as resp, open(get_pip_py, 'wb') as fh:
        fh.write(resp.read())
    z8cSqgZUDjUT([python, str(get_pip_py)])
    try:
        get_pip_py.unlink()
    except Exception:
        pass
if not _installed.exists():
    print('Установка зависимостей из requirements.txt…')
    z8cSqgZUDjUT([python, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
    if Path('requirements.txt').exists():
        z8cSqgZUDjUT([pip, 'install', '-r', 'requirements.txt'])
    z8cSqgZUDjUT([pip, 'install', 'psycopg2-binary'])
    _installed.write_text('ok')
if os.path.abspath(sys.executable) != os.path.abspath(python):
    print('Перезапуск из виртуального окружения…')
    os.execv(python, [python] + sys.argv)
Console = Console()

def init_alembic_env():
    alembic_env_py = Path('alembic/env.py')
    if alembic_env_py.exists():
        print('ℹAlembic инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    subprocess.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if alembic_env_py.exists():
        read_text = alembic_env_py.read_text()
        from_database_models_import_Base_from_config_import_DATABASE_URL_Заменяем_asyncpg_на_psycopg2_только_для_миграций_sync_url_DATABASE_URL_replace_postgresql_asyncpg_postgresql_psycopg2_config_set_main_option_sqlalchemy_url_sync_url_target_metadata_Base_metadata = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        alembic_env_py.write_text(read_text.replace('target_metadata = None', from_database_models_import_Base_from_config_import_DATABASE_URL_Заменяем_asyncpg_на_psycopg2_только_для_миграций_sync_url_DATABASE_URL_replace_postgresql_asyncpg_postgresql_psycopg2_config_set_main_option_sqlalchemy_url_sync_url_target_metadata_Base_metadata))
    print('✅ Alembic инициализирован.')

def cleanup_orphans():
    postgresql_psycopg2 = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    sync_url = create_engine(postgresql_psycopg2)
    try:
        with sync_url.connect() as conn:
            rowcount = conn.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            rowcount = conn.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            conn.commit()
        print(f'Очистка завершена. Удалено {rowcount} уведомлений и {rowcount} рефералов.')
    except Exception as exc:
        pass

def repair_alembic_version():
    api_main_app = Config('alembic.ini')
    cfg = ScriptDirectory.from_config(api_main_app)
    postgresql_psycopg2 = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    sync_url = create_engine(postgresql_psycopg2)
    with sync_url.connect() as conn:
        try:
            run = conn.execute(text('SELECT version_num FROM alembic_version'))
            scalar = run.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            cfg.get_revision(scalar)
        except Exception:
            print(f'Ревизия {scalar} отсутствует. Удаляем запись из alembic_version...')
            conn.execute(text('DELETE FROM alembic_version'))
            conn.commit()
            print('Запись alembic_version удалена. Миграции будут пересозданы.')
    subprocess.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**os.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def patch_alembic_env():
    alembic_env_py = Path('alembic/env.py')
    alembic_env_backup_py = Path('alembic/env_backup.py')
    if not alembic_env_py.exists():
        raise Exception('env.py не найден')
    shutil.copy(alembic_env_py, alembic_env_backup_py)
    read_text = alembic_env_py.read_text()
    _from_pathlib_import_Path_import_importlib_modules_dir_Path_modules_for_module_path_in_modules_dir_iterdir_if_module_path_models_py_exists_module_name_module_path_name_try_importlib_import_module_f_modules_module_name_models_except_Exception_as_e_print_f_Alembic_Ошибка_импорта_module_name_e_ = '\nfrom pathlib import Path\nimport importlib\n\nmodules_dir = Path("modules")\nfor module_path in modules_dir.iterdir():\n    if (module_path / "models.py").exists():\n        module_name = module_path.name\n        try:\n            importlib.import_module(f"modules.{module_name}.models")\n        except Exception as e:\n            print(f"[Alembic] ❌ Ошибка импорта {module_name}: {e}")\n'
    alembic_env_py.write_text(_from_pathlib_import_Path_import_importlib_modules_dir_Path_modules_for_module_path_in_modules_dir_iterdir_if_module_path_models_py_exists_module_name_module_path_name_try_importlib_import_module_f_modules_module_name_models_except_Exception_as_e_print_f_Alembic_Ошибка_импорта_module_name_e_ + '\n\n' + read_text)

def restore_alembic_env():
    alembic_env_py = Path('alembic/env.py')
    alembic_env_backup_py = Path('alembic/env_backup.py')
    if alembic_env_backup_py.exists():
        shutil.move(alembic_env_backup_py, alembic_env_py)

def run_migrations():
    print('Генерация и применение миграций...')
    cleanup_orphans()
    repair_alembic_version()
    run = subprocess.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in run.stdout:
        print('ℹИзменений в моделях нет — миграция не требуется.')
    else:
        print('Миграция создана. Применяем...')
        run = subprocess.run(['venv/bin/alembic', 'upgrade', 'head'], capture_output=1, text=1)
        if run.returncode != 0:
            print('❌ Ошибка при применении миграции:')
            print('STDOUT:', run.stdout)
            print('STDERR:', run.stderr)
            sys.exit(1)
    Console.print('[green] Alembic upgrade успешно выполнен.[/green]')

def migrate():
    init_alembic_env()
    alembic_versions = Path('alembic/versions')
    if not alembic_versions.exists():
        alembic_versions.mkdir(parents=1)
    patch_alembic_env()
    try:
        run_migrations()
    finally:
        restore_alembic_env()
migrate()

def install_cli():
    cli_launcher_py = os.path.abspath('cli_launcher.py')
    executable = sys.executable
    cS28M8tw6LfY = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    for phQQtM4ewpBI in cS28M8tw6LfY:
        if os.path.isdir(phQQtM4ewpBI) and os.access(phQQtM4ewpBI, os.W_OK):
            break
    else:
        return
    solobot = 'solobot'
    IAgR1dPl1T0C = solobot
    FN9v93eKE8N0 = os.path.join(phQQtM4ewpBI, IAgR1dPl1T0C)
    if os.path.exists(FN9v93eKE8N0):
        try:
            with open(FN9v93eKE8N0, 'r') as fh:
                read = fh.read()
            if cli_launcher_py in read:
                return
            else:
                print(f'⚠️ Команда `{IAgR1dPl1T0C}` уже установлена, но для другой копии бота.')
                strip = Ewhiwis92OU8('Введите другое имя команды (например, solobot-test): ').strip()
                if not strip:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                IAgR1dPl1T0C = strip
                FN9v93eKE8N0 = os.path.join(phQQtM4ewpBI, IAgR1dPl1T0C)
                if os.path.exists(FN9v93eKE8N0):
                    print(f'❌ Команда `{IAgR1dPl1T0C}` уже существует. Установка прервана.')
                    return
        except Exception as exc:
            print(f'⚠️ Ошибка при чтении команды {IAgR1dPl1T0C}: {exc}')
            return
    try:
        with open(FN9v93eKE8N0, 'w') as fh:
            fh.write(f"""#!/bin/bash\n'{executable}' '{cli_launcher_py}' "$@"\n""")
        os.chmod(FN9v93eKE8N0, 493)
        print(f'✅ Команда `{IAgR1dPl1T0C}` установлена! Используйте: {IAgR1dPl1T0C}')
    except Exception as exc:
        pass

async def backup_loop():
    oYIFHt95hx3G, = (importlib.import_module('utils.backup').backup_database.backup_database,)
    while True:
        await oYIFHt95hx3G()
        await asyncio.sleep(BACKUP_TIME)

async def api_server():
    api_main_app = uvicorn.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    cfg = uvicorn.Server(api_main_app)
    await cfg.serve()

async def on_startup(Application):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    await run_hooks('startup', bot=bot, dp=dp, app=Application, mode='prod', sessionmaker=async_session_maker)
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
    AsyncIOScheduler = AsyncIOScheduler()
    AsyncIOScheduler.add_job(send_stats, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    AsyncIOScheduler.start()

async def on_shutdown(Application):
    try:
        await run_hooks('shutdown', bot=bot, dp=dp, app=Application)
    except Exception as exc:
        logger.error(f'Ошибка shutdown-хуков: {exc}')
    await bot.delete_webhook()
    for task in asyncio.all_tasks():
        task.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as exc:
        logger.error(f'Ошибка при завершении работы: {exc}')

async def main():
    client_code_valid = await validate_client_code()
    if not client_code_valid:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        sys.exit(1)
    SOLO_ACCESS_KEY_B4TN_92QX_L7ME = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if MAIN_SECRET != SOLO_ACCESS_KEY_B4TN_92QX_L7ME:
        logger.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    register_middleware(dp, sessionmaker=async_session_maker)
    dp.include_router(router)
    dp.include_router(fallback_router)
    if DEV_MODE:
        logger.info('Запуск в режиме разработки...')
        await bot.delete_webhook()
        await init_db()
        await run_hooks('startup', bot=bot, dp=dp, app=None, mode='dev', sessionmaker=async_session_maker)
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
        try:
            await run_hooks('shutdown', bot=bot, dp=dp, app=None)
        except Exception as exc:
            logger.error(f'Ошибка shutdown-хуков (dev): {exc}')
        for task in bg_tasks:
            task.cancel()
        await asyncio.gather(*bg_tasks, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        Application = web.Application()
        Application['sessionmaker'] = async_session_maker
        Application.on_startup.append(on_startup)
        Application.on_shutdown.append(on_shutdown)
        if YOOKASSA_ENABLE:
            Application.router.add_post('/yookassa/webhook', yookassa_webhook)
        if YOOMONEY_ENABLE:
            Application.router.add_post('/yoomoney/webhook', yoomoney_webhook)
        if CRYPTO_BOT_ENABLE:
            Application.router.add_post('/cryptobot/webhook', cryptobot_webhook)
        if ROBOKASSA_ENABLE:
            Application.router.add_post('/robokassa/webhook', robokassa_webhook)
        if FREEKASSA_ENABLE:
            Application.router.add_get('/freekassa/webhook', freekassa_webhook)
        if TRIBUTE_ENABLE:
            Application.router.add_post('/tribute/webhook', tribute_webhook)
        Application.router.add_get(f'{SUB_PATH}{{email}}/{{tg_id}}', handle_subscription)
        await register_web_routes(Application.router)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(Application, path=WEBHOOK_PATH)
        setup_application(Application, dp, bot=bot)
        app = web.AppRunner(Application)
        await app.setup()
        runner = web.TCPSite(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await runner.start()
        if API_ENABLE:
            asyncio.create_task(api_server())
        logger.info(f'URL вебхука: {WEBHOOK_URL}')
        Event = asyncio.Event()
        get_event_loop = asyncio.get_event_loop()
        for jp5EZWTihCJs in (signal.SIGINT, signal.SIGTERM):
            get_event_loop.add_signal_handler(jp5EZWTihCJs, Event.set)
        try:
            await Event.wait()
        finally:
            pending = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
            for task in pending:
                try:
                    task.cancel()
                except Exception as exc:
                    logger.error(exc)
            await asyncio.gather(*pending, return_exceptions=1)
if zL5BH9evDcio == '__main__':
    install_cli()
    try:
        asyncio.run(main())
    except Exception as exc:
        logger.error(f'Ошибка при запуске приложения:\n{exc}')
