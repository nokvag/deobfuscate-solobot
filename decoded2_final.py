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
import venv
import importlib

def VLTILgCobR2q(HLMISGOoxhtq, SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy):
    try:
        return CJLS4yRqTzLB(HLMISGOoxhtq + '.' + SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
    except Exception:
        return CJLS4yRqTzLB(HLMISGOoxhtq, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
qSlLeyQ7VdNv = str(venv / 'bin' / 'python')
GEubzOScffp0 = str(venv / 'bin' / 'pip')
HizWI004zW0H = venv / '.installed'

def z8cSqgZUDjUT(TqUMzaW5W9NS, **afoXljZGRjuW):
    return subprocess.run(TqUMzaW5W9NS, check=1, **afoXljZGRjuW)
if not venv.exists():
    print('Создание виртуального окружения...')
    z8cSqgZUDjUT([sys.executable, '-m', 'venv', str(venv)])
try:
    z8cSqgZUDjUT([qSlLeyQ7VdNv, '-m', 'ensurepip', '--upgrade'])
except Exception:
    print('ensurepip недоступен, качаю get-pip.py…')
    ADrQh6Q0Xq4n = venv / 'get-pip.py'
    with request.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=30) as wI5a6NtuIHOG, open(ADrQh6Q0Xq4n, 'wb') as VD5XtVzFLHb2:
        VD5XtVzFLHb2.write(wI5a6NtuIHOG.read())
    z8cSqgZUDjUT([qSlLeyQ7VdNv, str(ADrQh6Q0Xq4n)])
    try:
        ADrQh6Q0Xq4n.unlink()
    except Exception:
        pass
if not HizWI004zW0H.exists():
    print('Установка зависимостей из requirements.txt…')
    z8cSqgZUDjUT([qSlLeyQ7VdNv, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
    if Path('requirements.txt').exists():
        z8cSqgZUDjUT([GEubzOScffp0, 'install', '-r', 'requirements.txt'])
    z8cSqgZUDjUT([GEubzOScffp0, 'install', 'psycopg2-binary'])
    HizWI004zW0H.write_text('ok')
if os.path.abspath(sys.executable) != os.path.abspath(qSlLeyQ7VdNv):
    print('Перезапуск из виртуального окружения…')
    os.execv(qSlLeyQ7VdNv, [qSlLeyQ7VdNv] + sys.argv)
gRRvVbYhM0LB = Console()

def Pib7Isbe5Piv():
    alembic_env_path = Path('alembic/env.py')
    if alembic_env_path.exists():
        print('ℹAlembic инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    subprocess.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if alembic_env_path.exists():
        fvX0NPd8gKqD = alembic_env_path.read_text()
        dvrwJuLJSlIR = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        alembic_env_path.write_text(fvX0NPd8gKqD.replace('target_metadata = None', dvrwJuLJSlIR))
    print('✅ Alembic инициализирован.')

def Yx6Nrcbtb4PN():
    xqQbR3mcDJZE = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    engine = create_engine(xqQbR3mcDJZE)
    try:
        with engine.connect() as conn:
            Erx7KqRlGK6W = conn.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            dWyzIwk5ehXI = conn.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            conn.commit()
        print(f'Очистка завершена. Удалено {Erx7KqRlGK6W} уведомлений и {dWyzIwk5ehXI} рефералов.')
    except Exception as exc:
        pass

def ot1STj0Fihnd():
    config = Config('alembic.ini')
    script_dir = ScriptDirectory.from_config(config)
    xqQbR3mcDJZE = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    engine = create_engine(xqQbR3mcDJZE)
    with engine.connect() as conn:
        try:
            FCcaVPw_BfBa = conn.execute(text('SELECT version_num FROM alembic_version'))
            v8h0Nrd1Zgij = FCcaVPw_BfBa.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            script_dir.get_revision(v8h0Nrd1Zgij)
        except Exception:
            print(f'Ревизия {v8h0Nrd1Zgij} отсутствует. Удаляем запись из alembic_version...')
            conn.execute(text('DELETE FROM alembic_version'))
            conn.commit()
            print('Запись alembic_version удалена. Миграции будут пересозданы.')
    subprocess.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**os.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def NrMxwt71pAGc():
    alembic_env_path = Path('alembic/env.py')
    path = Path('alembic/env_backup.py')
    if not alembic_env_path.exists():
        raise kkr6asGQBbL4('env.py не найден')
    shutil.copy(alembic_env_path, path)
    GAGG3SzhZoAk = alembic_env_path.read_text()
    path_2 = '\nfrom pathlib import Path\nimport importlib\n\nmodules_dir = Path("modules")\nfor module_path in modules_dir.iterdir():\n    if (module_path / "models.py").exists():\n        module_name = module_path.name\n        try:\n            importlib.import_module(f"modules.{module_name}.models")\n        except Exception as e:\n            print(f"[Alembic] ❌ Ошибка импорта {module_name}: {e}")\n'
    alembic_env_path.write_text(path_2 + '\n\n' + GAGG3SzhZoAk)

def o2KdGgnRtgxA():
    alembic_env_path = Path('alembic/env.py')
    path = Path('alembic/env_backup.py')
    if path.exists():
        shutil.move(path, alembic_env_path)

def yfTW9tS0_kHo():
    print('Генерация и применение миграций...')
    Yx6Nrcbtb4PN()
    ot1STj0Fihnd()
    FCcaVPw_BfBa = subprocess.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in FCcaVPw_BfBa.stdout:
        print('ℹИзменений в моделях нет — миграция не требуется.')
    else:
        print('Миграция создана. Применяем...')
        LVPFufwjktJF = subprocess.run(['venv/bin/alembic', 'upgrade', 'head'], capture_output=1, text=1)
        if LVPFufwjktJF.returncode != 0:
            print('❌ Ошибка при применении миграции:')
            print('STDOUT:', LVPFufwjktJF.stdout)
            print('STDERR:', LVPFufwjktJF.stderr)
            sys.exit(1)
    gRRvVbYhM0LB.print('[green] Alembic upgrade успешно выполнен.[/green]')

def bqBdUDQyD_PG():
    Pib7Isbe5Piv()
    vufHelYUYpjq = Path('alembic/versions')
    if not vufHelYUYpjq.exists():
        vufHelYUYpjq.mkdir(parents=1)
    NrMxwt71pAGc()
    try:
        yfTW9tS0_kHo()
    finally:
        o2KdGgnRtgxA()
bqBdUDQyD_PG()

def XpF3sTj6yajP():
    sXk2F8EV6LJl = os.path.abspath('cli_launcher.py')
    MtRx3rujhwU4 = sys.executable
    cS28M8tw6LfY = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    for phQQtM4ewpBI in cS28M8tw6LfY:
        if os.path.isdir(phQQtM4ewpBI) and os.access(phQQtM4ewpBI, os.W_OK):
            break
    else:
        return
    Yl4j1ojn1GBh = 'solobot'
    FN9v93eKE8N0 = Yl4j1ojn1GBh
    HBWnJvBDhafr = os.path.join(phQQtM4ewpBI, FN9v93eKE8N0)
    if os.path.exists(HBWnJvBDhafr):
        try:
            with open(HBWnJvBDhafr, 'r') as VD5XtVzFLHb2:
                H2TNCRVK_JON = VD5XtVzFLHb2.read()
            if sXk2F8EV6LJl in H2TNCRVK_JON:
                return
            else:
                print(f'⚠️ Команда `{FN9v93eKE8N0}` уже установлена, но для другой копии бота.')
                IAgR1dPl1T0C = Ewhiwis92OU8('Введите другое имя команды (например, solobot-test): ').strip()
                if not IAgR1dPl1T0C:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                FN9v93eKE8N0 = IAgR1dPl1T0C
                HBWnJvBDhafr = os.path.join(phQQtM4ewpBI, FN9v93eKE8N0)
                if os.path.exists(HBWnJvBDhafr):
                    print(f'❌ Команда `{FN9v93eKE8N0}` уже существует. Установка прервана.')
                    return
        except Exception as exc:
            print(f'⚠️ Ошибка при чтении команды {FN9v93eKE8N0}: {exc}')
            return
    try:
        with open(HBWnJvBDhafr, 'w') as VD5XtVzFLHb2:
            VD5XtVzFLHb2.write(f"""#!/bin/bash\n'{MtRx3rujhwU4}' '{sXk2F8EV6LJl}' "$@"\n""")
        os.chmod(HBWnJvBDhafr, 493)
        print(f'✅ Команда `{FN9v93eKE8N0}` установлена! Используйте: {FN9v93eKE8N0}')
    except Exception as exc:
        pass

async def wM4UKfLL5p4k():
    (oYIFHt95hx3G,) = (VLTILgCobR2q('utils.backup', 'backup_database', globals=None, locals=None, level=0).backup.backup_database,)
    while True:
        await oYIFHt95hx3G()
        await asyncio.sleep(BACKUP_TIME)

async def RnhunT1Pokyl():
    config = uvicorn.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    server = uvicorn.Server(config)
    await server.serve()

async def M7xmJlQpYzNB(Kzqgqt2OnbBD):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    await run_hooks('startup', bot=bot, dp=dp, app=Kzqgqt2OnbBD, mode='prod', sessionmaker=async_session_maker)
    asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))
    if BACKUP_TIME > 0:
        asyncio.create_task(wM4UKfLL5p4k())
    if PING_TIME > 0:

        async def aNXQRddvjV1V():
            async with async_session_maker() as hpuZ2br8L5KF:
                await check_servers(hpuZ2br8L5KF)
        asyncio.create_task(aNXQRddvjV1V())

    async def WaZ61jx33zZR():
        async with async_session_maker() as hpuZ2br8L5KF:
            await send_daily_stats_report(hpuZ2br8L5KF)
    fVTKKdPXSc0s = AsyncIOScheduler()
    fVTKKdPXSc0s.add_job(WaZ61jx33zZR, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    fVTKKdPXSc0s.start()

async def Fklfk5LsFLlG(Kzqgqt2OnbBD):
    try:
        await run_hooks('shutdown', bot=bot, dp=dp, app=Kzqgqt2OnbBD)
    except Exception as exc:
        logger.error(f'Ошибка shutdown-хуков: {exc}')
    await bot.delete_webhook()
    for TQCuJzXXjNfR in asyncio.all_tasks():
        TQCuJzXXjNfR.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as exc:
        logger.error(f'Ошибка при завершении работы: {exc}')

async def YyFOxjswwO6V(Wg4y0tl9UCps):
    logger.info('Остановка вебхуков...')
    await site.stop()
    logger.info('Остановка бота.')

async def of1m0QeKOPMV():
    Y3MtP52LbSQz = await validate_client_code()
    if not Y3MtP52LbSQz:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        sys.exit(1)
    CFNWNYjIE8CO = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if MAIN_SECRET != CFNWNYjIE8CO:
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
        NZRpUosWW30x = [asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))]
        if PING_TIME > 0:

            async def aNXQRddvjV1V():
                async with async_session_maker() as hpuZ2br8L5KF:
                    await check_servers(hpuZ2br8L5KF)
            NZRpUosWW30x.append(asyncio.create_task(aNXQRddvjV1V()))
        if BACKUP_TIME > 0:
            NZRpUosWW30x.append(asyncio.create_task(wM4UKfLL5p4k()))
        if API_ENABLE:
            logger.info('🔧 DEV: Запускаем API...')
            mq7VdOSYsKxq = [sys.executable, '-m', 'uvicorn', 'api.main:app', '--host', API_HOST, '--port', str(API_PORT), '--reload']
            if not API_LOGGING:
                mq7VdOSYsKxq += ['--log-level', 'critical']
            subprocess.Popen(mq7VdOSYsKxq)
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        try:
            await run_hooks('shutdown', bot=bot, dp=dp, app=None)
        except Exception as exc:
            logger.error(f'Ошибка shutdown-хуков (dev): {exc}')
        for TQCuJzXXjNfR in NZRpUosWW30x:
            TQCuJzXXjNfR.cancel()
        await asyncio.gather(*NZRpUosWW30x, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        Kzqgqt2OnbBD = web.Application()
        Kzqgqt2OnbBD['sessionmaker'] = async_session_maker
        Kzqgqt2OnbBD.on_startup.append(M7xmJlQpYzNB)
        Kzqgqt2OnbBD.on_shutdown.append(Fklfk5LsFLlG)
        if YOOKASSA_ENABLE:
            Kzqgqt2OnbBD.router.add_post('/yookassa/webhook', yookassa_webhook)
        if YOOMONEY_ENABLE:
            Kzqgqt2OnbBD.router.add_post('/yoomoney/webhook', yoomoney_webhook)
        if CRYPTO_BOT_ENABLE:
            Kzqgqt2OnbBD.router.add_post('/cryptobot/webhook', cryptobot_webhook)
        if ROBOKASSA_ENABLE:
            Kzqgqt2OnbBD.router.add_post('/robokassa/webhook', robokassa_webhook)
        if FREEKASSA_ENABLE:
            Kzqgqt2OnbBD.router.add_get('/freekassa/webhook', freekassa_webhook)
        if TRIBUTE_ENABLE:
            Kzqgqt2OnbBD.router.add_post('/tribute/webhook', tribute_webhook)
        Kzqgqt2OnbBD.router.add_get(f'{BqOreXERAvWV}{{email}}/{{tg_id}}', handle_subscription)
        await register_web_routes(Kzqgqt2OnbBD.router)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(Kzqgqt2OnbBD, path=WEBHOOK_PATH)
        setup_application(Kzqgqt2OnbBD, dp, bot=bot)
        runner = web.AppRunner(Kzqgqt2OnbBD)
        await runner.setup()
        site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await site.start()
        if API_ENABLE:
            asyncio.create_task(RnhunT1Pokyl())
        logger.info(f'URL вебхука: {g_ErmwCpaF7a}')
        pXePuUjRPloW = asyncio.Event()
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, pXePuUjRPloW.set)
        try:
            await pXePuUjRPloW.wait()
        finally:
            q0B7Jzr9PNTf = [TQCuJzXXjNfR for TQCuJzXXjNfR in asyncio.all_tasks() if TQCuJzXXjNfR is not asyncio.current_task()]
            for TQCuJzXXjNfR in q0B7Jzr9PNTf:
                try:
                    TQCuJzXXjNfR.cancel()
                except Exception as exc:
                    logger.error(exc)
            await asyncio.gather(*q0B7Jzr9PNTf, return_exceptions=1)
if zL5BH9evDcio == '__main__':
    XpF3sTj6yajP()
    try:
        asyncio.run(of1m0QeKOPMV())
    except Exception as exc:
        logger.error(f'Ошибка при запуске приложения:\n{exc}')
