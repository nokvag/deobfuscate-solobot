import importlib

def VLTILgCobR2q(HLMISGOoxhtq, SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy):
    try:
        return CJLS4yRqTzLB(HLMISGOoxhtq + '.' + SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
    except Exception:
        return CJLS4yRqTzLB(HLMISGOoxhtq, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
(l_shM1eICFqR,) = (CJLS4yRqTzLB('os'),)
(y7TRXgJ4_d2f,) = (CJLS4yRqTzLB('sys'),)
(euouZ_Eo2CGc,) = (CJLS4yRqTzLB('subprocess'),)
(Path,) = (VLTILgCobR2q('pathlib', 'Path', globals=None, locals=None, level=0).Path,)
(wf3b04nBTB0M,) = (CJLS4yRqTzLB('urllib.request'),)
KOMvfYWvxpvB = Path('venv')
qSlLeyQ7VdNv = str(KOMvfYWvxpvB / 'bin' / 'python')
GEubzOScffp0 = str(KOMvfYWvxpvB / 'bin' / 'pip')
HizWI004zW0H = KOMvfYWvxpvB / '.installed'

def z8cSqgZUDjUT(TqUMzaW5W9NS, **afoXljZGRjuW):
    return euouZ_Eo2CGc.run(TqUMzaW5W9NS, check=1, **afoXljZGRjuW)
if not KOMvfYWvxpvB.exists():
    print('Создание виртуального окружения...')
    z8cSqgZUDjUT([y7TRXgJ4_d2f.executable, '-m', 'venv', str(KOMvfYWvxpvB)])
try:
    z8cSqgZUDjUT([qSlLeyQ7VdNv, '-m', 'ensurepip', '--upgrade'])
except Exception:
    print('ensurepip недоступен, качаю get-pip.py…')
    ADrQh6Q0Xq4n = KOMvfYWvxpvB / 'get-pip.py'
    with wf3b04nBTB0M.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=30) as wI5a6NtuIHOG, open(ADrQh6Q0Xq4n, 'wb') as VD5XtVzFLHb2:
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
if l_shM1eICFqR.path.abspath(y7TRXgJ4_d2f.executable) != l_shM1eICFqR.path.abspath(qSlLeyQ7VdNv):
    print('Перезапуск из виртуального окружения…')
    l_shM1eICFqR.execv(qSlLeyQ7VdNv, [qSlLeyQ7VdNv] + y7TRXgJ4_d2f.argv)
(Console,) = (VLTILgCobR2q('rich.console', 'Console', globals=None, locals=None, level=0).console.Console,)
gRRvVbYhM0LB = Console()
(create_engine, text) = (VLTILgCobR2q('sqlalchemy', 'create_engine', globals=None, locals=None, level=0).create_engine, VLTILgCobR2q('sqlalchemy', 'text', globals=None, locals=None, level=0).text)
(Config,) = (VLTILgCobR2q('alembic.config', 'Config', globals=None, locals=None, level=0).config.Config,)
(ScriptDirectory,) = (VLTILgCobR2q('alembic.script', 'ScriptDirectory', globals=None, locals=None, level=0).script.ScriptDirectory,)
(DATABASE_URL,) = (VLTILgCobR2q('config', 'DATABASE_URL', globals=None, locals=None, level=0).DATABASE_URL,)

def Pib7Isbe5Piv():
    i_5gN_6A5Aqj = Path('alembic/env.py')
    if i_5gN_6A5Aqj.exists():
        print('ℹAlembic инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    euouZ_Eo2CGc.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if i_5gN_6A5Aqj.exists():
        fvX0NPd8gKqD = i_5gN_6A5Aqj.read_text()
        dvrwJuLJSlIR = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        i_5gN_6A5Aqj.write_text(fvX0NPd8gKqD.replace('target_metadata = None', dvrwJuLJSlIR))
    print('✅ Alembic инициализирован.')

def Yx6Nrcbtb4PN():
    xqQbR3mcDJZE = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    ya1W7oAVx8Q4 = create_engine(xqQbR3mcDJZE)
    try:
        with ya1W7oAVx8Q4.connect() as y3mYlbnvULnu:
            Erx7KqRlGK6W = y3mYlbnvULnu.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            dWyzIwk5ehXI = y3mYlbnvULnu.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            y3mYlbnvULnu.commit()
        print(f'Очистка завершена. Удалено {Erx7KqRlGK6W} уведомлений и {dWyzIwk5ehXI} рефералов.')
    except Exception as umvpgGZGd92J:
        pass

def ot1STj0Fihnd():
    CRFlXIWSq7W1 = Config('alembic.ini')
    fkMzg2r6XODx = ScriptDirectory.from_config(CRFlXIWSq7W1)
    xqQbR3mcDJZE = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    ya1W7oAVx8Q4 = create_engine(xqQbR3mcDJZE)
    with ya1W7oAVx8Q4.connect() as y3mYlbnvULnu:
        try:
            FCcaVPw_BfBa = y3mYlbnvULnu.execute(text('SELECT version_num FROM alembic_version'))
            v8h0Nrd1Zgij = FCcaVPw_BfBa.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            fkMzg2r6XODx.get_revision(v8h0Nrd1Zgij)
        except Exception:
            print(f'Ревизия {v8h0Nrd1Zgij} отсутствует. Удаляем запись из alembic_version...')
            y3mYlbnvULnu.execute(text('DELETE FROM alembic_version'))
            y3mYlbnvULnu.commit()
            print('Запись alembic_version удалена. Миграции будут пересозданы.')
    euouZ_Eo2CGc.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**l_shM1eICFqR.environ, 'ALEMBIC_SAFE_BOOT': '1'})
(TAq23VlWMJNj,) = (CJLS4yRqTzLB('shutil'),)

def NrMxwt71pAGc():
    i_5gN_6A5Aqj = Path('alembic/env.py')
    P2gKpi9RnARy = Path('alembic/env_backup.py')
    if not i_5gN_6A5Aqj.exists():
        raise kkr6asGQBbL4('env.py не найден')
    TAq23VlWMJNj.copy(i_5gN_6A5Aqj, P2gKpi9RnARy)
    GAGG3SzhZoAk = i_5gN_6A5Aqj.read_text()
    guKuVpoPOUK0 = '\nfrom pathlib import Path\nimport importlib\n\nmodules_dir = Path("modules")\nfor module_path in modules_dir.iterdir():\n    if (module_path / "models.py").exists():\n        module_name = module_path.name\n        try:\n            importlib.import_module(f"modules.{module_name}.models")\n        except Exception as e:\n            print(f"[Alembic] ❌ Ошибка импорта {module_name}: {e}")\n'
    i_5gN_6A5Aqj.write_text(guKuVpoPOUK0 + '\n\n' + GAGG3SzhZoAk)

def o2KdGgnRtgxA():
    i_5gN_6A5Aqj = Path('alembic/env.py')
    P2gKpi9RnARy = Path('alembic/env_backup.py')
    if P2gKpi9RnARy.exists():
        TAq23VlWMJNj.move(P2gKpi9RnARy, i_5gN_6A5Aqj)

def yfTW9tS0_kHo():
    print('Генерация и применение миграций...')
    Yx6Nrcbtb4PN()
    ot1STj0Fihnd()
    FCcaVPw_BfBa = euouZ_Eo2CGc.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in FCcaVPw_BfBa.stdout:
        print('ℹИзменений в моделях нет — миграция не требуется.')
    else:
        print('Миграция создана. Применяем...')
        LVPFufwjktJF = euouZ_Eo2CGc.run(['venv/bin/alembic', 'upgrade', 'head'], capture_output=1, text=1)
        if LVPFufwjktJF.returncode != 0:
            print('❌ Ошибка при применении миграции:')
            print('STDOUT:', LVPFufwjktJF.stdout)
            print('STDERR:', LVPFufwjktJF.stderr)
            y7TRXgJ4_d2f.exit(1)
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
(yoJVaScdKjmf,) = (CJLS4yRqTzLB('asyncio'),)
(l_shM1eICFqR,) = (CJLS4yRqTzLB('os'),)
(AJA4Z4tIYF55,) = (CJLS4yRqTzLB('signal'),)
(euouZ_Eo2CGc,) = (CJLS4yRqTzLB('subprocess'),)
(y7TRXgJ4_d2f,) = (CJLS4yRqTzLB('sys'),)
(wjA9ZLNDdMfq,) = (CJLS4yRqTzLB('uvicorn'),)
(SimpleRequestHandler, setup_application) = (VLTILgCobR2q('aiogram.webhook.aiohttp_server', 'SimpleRequestHandler', globals=None, locals=None, level=0).webhook.aiohttp_server.SimpleRequestHandler, VLTILgCobR2q('aiogram.webhook.aiohttp_server', 'setup_application', globals=None, locals=None, level=0).webhook.aiohttp_server.setup_application)
(web,) = (VLTILgCobR2q('aiohttp', 'web', globals=None, locals=None, level=0).web,)
(AsyncIOScheduler,) = (VLTILgCobR2q('apscheduler.schedulers.asyncio', 'AsyncIOScheduler', globals=None, locals=None, level=0).schedulers.asyncio.AsyncIOScheduler,)
(CronTrigger,) = (VLTILgCobR2q('apscheduler.triggers.cron', 'CronTrigger', globals=None, locals=None, level=0).triggers.cron.CronTrigger,)
(bot, dp) = (VLTILgCobR2q('bot', 'bot', globals=None, locals=None, level=0).bot, VLTILgCobR2q('bot', 'dp', globals=None, locals=None, level=0).dp)
(BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, PING_TIME, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, API_ENABLE, API_HOST, API_PORT, API_LOGGING, FREEKASSA_ENABLE, TRIBUTE_ENABLE) = (VLTILgCobR2q('config', 'BACKUP_TIME', globals=None, locals=None, level=0).BACKUP_TIME, VLTILgCobR2q('config', 'CRYPTO_BOT_ENABLE', globals=None, locals=None, level=0).CRYPTO_BOT_ENABLE, VLTILgCobR2q('config', 'DEV_MODE', globals=None, locals=None, level=0).DEV_MODE, VLTILgCobR2q('config', 'PING_TIME', globals=None, locals=None, level=0).PING_TIME, VLTILgCobR2q('config', 'ROBOKASSA_ENABLE', globals=None, locals=None, level=0).ROBOKASSA_ENABLE, VLTILgCobR2q('config', 'SUB_PATH', globals=None, locals=None, level=0).SUB_PATH, VLTILgCobR2q('config', 'WEBAPP_HOST', globals=None, locals=None, level=0).WEBAPP_HOST, VLTILgCobR2q('config', 'WEBAPP_PORT', globals=None, locals=None, level=0).WEBAPP_PORT, VLTILgCobR2q('config', 'WEBHOOK_PATH', globals=None, locals=None, level=0).WEBHOOK_PATH, VLTILgCobR2q('config', 'WEBHOOK_URL', globals=None, locals=None, level=0).WEBHOOK_URL, VLTILgCobR2q('config', 'YOOKASSA_ENABLE', globals=None, locals=None, level=0).YOOKASSA_ENABLE, VLTILgCobR2q('config', 'YOOMONEY_ENABLE', globals=None, locals=None, level=0).YOOMONEY_ENABLE, VLTILgCobR2q('config', 'API_ENABLE', globals=None, locals=None, level=0).API_ENABLE, VLTILgCobR2q('config', 'API_HOST', globals=None, locals=None, level=0).API_HOST, VLTILgCobR2q('config', 'API_PORT', globals=None, locals=None, level=0).API_PORT, VLTILgCobR2q('config', 'API_LOGGING', globals=None, locals=None, level=0).API_LOGGING, VLTILgCobR2q('config', 'FREEKASSA_ENABLE', globals=None, locals=None, level=0).FREEKASSA_ENABLE, VLTILgCobR2q('config', 'TRIBUTE_ENABLE', globals=None, locals=None, level=0).TRIBUTE_ENABLE)
(async_session_maker, init_db) = (VLTILgCobR2q('database', 'async_session_maker', globals=None, locals=None, level=0).async_session_maker, VLTILgCobR2q('database', 'init_db', globals=None, locals=None, level=0).init_db)
(router,) = (VLTILgCobR2q('handlers', 'router', globals=None, locals=None, level=0).router,)
(send_daily_stats_report,) = (VLTILgCobR2q('handlers.admin.stats.stats_handler', 'send_daily_stats_report', globals=None, locals=None, level=0).admin.stats.stats_handler.send_daily_stats_report,)
(fallback_router,) = (VLTILgCobR2q('handlers.fallback_router', 'fallback_router', globals=None, locals=None, level=0).fallback_router.fallback_router,)
(handle_subscription,) = (VLTILgCobR2q('handlers.keys.subscriptions', 'handle_subscription', globals=None, locals=None, level=0).keys.subscriptions.handle_subscription,)
(periodic_notifications,) = (VLTILgCobR2q('handlers.notifications.general_notifications', 'periodic_notifications', globals=None, locals=None, level=0).notifications.general_notifications.periodic_notifications,)
(cryptobot_webhook,) = (VLTILgCobR2q('handlers.payments.cryprobot_pay', 'cryptobot_webhook', globals=None, locals=None, level=0).payments.cryprobot_pay.cryptobot_webhook,)
(tribute_webhook,) = (VLTILgCobR2q('handlers.payments.tribute_pay', 'tribute_webhook', globals=None, locals=None, level=0).payments.tribute_pay.tribute_webhook,)
(validate_client_code,) = (VLTILgCobR2q('handlers.payments.gift', 'validate_client_code', globals=None, locals=None, level=0).payments.gift.validate_client_code,)
(robokassa_webhook,) = (VLTILgCobR2q('handlers.payments.robokassa_pay', 'robokassa_webhook', globals=None, locals=None, level=0).payments.robokassa_pay.robokassa_webhook,)
(MAIN_SECRET, yookassa_webhook) = (VLTILgCobR2q('handlers.payments.yookassa_pay', 'MAIN_SECRET', globals=None, locals=None, level=0).payments.yookassa_pay.MAIN_SECRET, VLTILgCobR2q('handlers.payments.yookassa_pay', 'yookassa_webhook', globals=None, locals=None, level=0).payments.yookassa_pay.yookassa_webhook)
(yoomoney_webhook,) = (VLTILgCobR2q('handlers.payments.yoomoney_pay', 'yoomoney_webhook', globals=None, locals=None, level=0).payments.yoomoney_pay.yoomoney_webhook,)
(freekassa_webhook,) = (VLTILgCobR2q('handlers.payments.freekassa_pay', 'freekassa_webhook', globals=None, locals=None, level=0).payments.freekassa_pay.freekassa_webhook,)
(logger,) = (VLTILgCobR2q('logger', 'logger', globals=None, locals=None, level=0).logger,)
(register_middleware,) = (VLTILgCobR2q('middlewares', 'register_middleware', globals=None, locals=None, level=0).register_middleware,)
(check_servers,) = (VLTILgCobR2q('servers', 'check_servers', globals=None, locals=None, level=0).check_servers,)
(register_web_routes,) = (VLTILgCobR2q('web', 'register_web_routes', globals=None, locals=None, level=0).register_web_routes,)
(run_hooks,) = (VLTILgCobR2q('hooks.hooks', 'run_hooks', globals=None, locals=None, level=0).hooks.run_hooks,)

def XpF3sTj6yajP():
    sXk2F8EV6LJl = l_shM1eICFqR.path.abspath('cli_launcher.py')
    MtRx3rujhwU4 = y7TRXgJ4_d2f.executable
    cS28M8tw6LfY = ['/usr/local/bin', '/usr/bin', l_shM1eICFqR.path.expanduser('~/.local/bin')]
    for phQQtM4ewpBI in cS28M8tw6LfY:
        if l_shM1eICFqR.path.isdir(phQQtM4ewpBI) and l_shM1eICFqR.access(phQQtM4ewpBI, l_shM1eICFqR.W_OK):
            break
    else:
        return
    Yl4j1ojn1GBh = 'solobot'
    FN9v93eKE8N0 = Yl4j1ojn1GBh
    HBWnJvBDhafr = l_shM1eICFqR.path.join(phQQtM4ewpBI, FN9v93eKE8N0)
    if l_shM1eICFqR.path.exists(HBWnJvBDhafr):
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
                HBWnJvBDhafr = l_shM1eICFqR.path.join(phQQtM4ewpBI, FN9v93eKE8N0)
                if l_shM1eICFqR.path.exists(HBWnJvBDhafr):
                    print(f'❌ Команда `{FN9v93eKE8N0}` уже существует. Установка прервана.')
                    return
        except Exception as umvpgGZGd92J:
            print(f'⚠️ Ошибка при чтении команды {FN9v93eKE8N0}: {umvpgGZGd92J}')
            return
    try:
        with open(HBWnJvBDhafr, 'w') as VD5XtVzFLHb2:
            VD5XtVzFLHb2.write(f"""#!/bin/bash\n'{MtRx3rujhwU4}' '{sXk2F8EV6LJl}' "$@"\n""")
        l_shM1eICFqR.chmod(HBWnJvBDhafr, 493)
        print(f'✅ Команда `{FN9v93eKE8N0}` установлена! Используйте: {FN9v93eKE8N0}')
    except Exception as umvpgGZGd92J:
        pass

async def wM4UKfLL5p4k():
    (oYIFHt95hx3G,) = (VLTILgCobR2q('utils.backup', 'backup_database', globals=None, locals=None, level=0).backup.backup_database,)
    while 1:
        await oYIFHt95hx3G()
        await yoJVaScdKjmf.sleep(BACKUP_TIME)

async def RnhunT1Pokyl():
    CRFlXIWSq7W1 = wjA9ZLNDdMfq.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    bVWK7XMx6YQ8 = wjA9ZLNDdMfq.Server(CRFlXIWSq7W1)
    await bVWK7XMx6YQ8.serve()

async def M7xmJlQpYzNB(Kzqgqt2OnbBD):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    await run_hooks('startup', bot=bot, dp=dp, app=Kzqgqt2OnbBD, mode='prod', sessionmaker=async_session_maker)
    yoJVaScdKjmf.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))
    if BACKUP_TIME > 0:
        yoJVaScdKjmf.create_task(wM4UKfLL5p4k())
    if PING_TIME > 0:

        async def aNXQRddvjV1V():
            async with async_session_maker() as hpuZ2br8L5KF:
                await check_servers(hpuZ2br8L5KF)
        yoJVaScdKjmf.create_task(aNXQRddvjV1V())

    async def WaZ61jx33zZR():
        async with async_session_maker() as hpuZ2br8L5KF:
            await send_daily_stats_report(hpuZ2br8L5KF)
    fVTKKdPXSc0s = AsyncIOScheduler()
    fVTKKdPXSc0s.add_job(WaZ61jx33zZR, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    fVTKKdPXSc0s.start()

async def Fklfk5LsFLlG(Kzqgqt2OnbBD):
    try:
        await run_hooks('shutdown', bot=bot, dp=dp, app=Kzqgqt2OnbBD)
    except Exception as umvpgGZGd92J:
        logger.error(f'Ошибка shutdown-хуков: {umvpgGZGd92J}')
    await bot.delete_webhook()
    for TQCuJzXXjNfR in yoJVaScdKjmf.all_tasks():
        TQCuJzXXjNfR.cancel()
    try:
        await yoJVaScdKjmf.gather(*yoJVaScdKjmf.all_tasks(), return_exceptions=1)
    except Exception as umvpgGZGd92J:
        logger.error(f'Ошибка при завершении работы: {umvpgGZGd92J}')

async def YyFOxjswwO6V(Wg4y0tl9UCps):
    logger.info('Остановка вебхуков...')
    await Wg4y0tl9UCps.stop()
    logger.info('Остановка бота.')

async def of1m0QeKOPMV():
    Y3MtP52LbSQz = await validate_client_code()
    if not Y3MtP52LbSQz:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        y7TRXgJ4_d2f.exit(1)
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
        NZRpUosWW30x = [yoJVaScdKjmf.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))]
        if PING_TIME > 0:

            async def aNXQRddvjV1V():
                async with async_session_maker() as hpuZ2br8L5KF:
                    await check_servers(hpuZ2br8L5KF)
            NZRpUosWW30x.append(yoJVaScdKjmf.create_task(aNXQRddvjV1V()))
        if BACKUP_TIME > 0:
            NZRpUosWW30x.append(yoJVaScdKjmf.create_task(wM4UKfLL5p4k()))
        if API_ENABLE:
            logger.info('🔧 DEV: Запускаем API...')
            mq7VdOSYsKxq = [y7TRXgJ4_d2f.executable, '-m', 'uvicorn', 'api.main:app', '--host', API_HOST, '--port', str(API_PORT), '--reload']
            if not API_LOGGING:
                mq7VdOSYsKxq += ['--log-level', 'critical']
            euouZ_Eo2CGc.Popen(mq7VdOSYsKxq)
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        try:
            await run_hooks('shutdown', bot=bot, dp=dp, app=None)
        except Exception as umvpgGZGd92J:
            logger.error(f'Ошибка shutdown-хуков (dev): {umvpgGZGd92J}')
        for TQCuJzXXjNfR in NZRpUosWW30x:
            TQCuJzXXjNfR.cancel()
        await yoJVaScdKjmf.gather(*NZRpUosWW30x, return_exceptions=1)
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
        JUE22Ecu3lXC = web.AppRunner(Kzqgqt2OnbBD)
        await JUE22Ecu3lXC.setup()
        Wg4y0tl9UCps = web.TCPSite(JUE22Ecu3lXC, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await Wg4y0tl9UCps.start()
        if API_ENABLE:
            yoJVaScdKjmf.create_task(RnhunT1Pokyl())
        logger.info(f'URL вебхука: {g_ErmwCpaF7a}')
        pXePuUjRPloW = yoJVaScdKjmf.Event()
        WwAfJLQPh73Q = yoJVaScdKjmf.get_event_loop()
        for jp5EZWTihCJs in (AJA4Z4tIYF55.SIGINT, AJA4Z4tIYF55.SIGTERM):
            WwAfJLQPh73Q.add_signal_handler(jp5EZWTihCJs, pXePuUjRPloW.set)
        try:
            await pXePuUjRPloW.wait()
        finally:
            q0B7Jzr9PNTf = [TQCuJzXXjNfR for TQCuJzXXjNfR in yoJVaScdKjmf.all_tasks() if TQCuJzXXjNfR is not yoJVaScdKjmf.current_task()]
            for TQCuJzXXjNfR in q0B7Jzr9PNTf:
                try:
                    TQCuJzXXjNfR.cancel()
                except Exception as umvpgGZGd92J:
                    logger.error(umvpgGZGd92J)
            await yoJVaScdKjmf.gather(*q0B7Jzr9PNTf, return_exceptions=1)
if zL5BH9evDcio == '__main__':
    XpF3sTj6yajP()
    try:
        yoJVaScdKjmf.run(of1m0QeKOPMV())
    except Exception as umvpgGZGd92J:
        logger.error(f'Ошибка при запуске приложения:\n{umvpgGZGd92J}')