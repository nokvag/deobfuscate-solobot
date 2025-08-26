import importlib

def VLTILgCobR2q(HLMISGOoxhtq, SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy):
    try:
        return CJLS4yRqTzLB(HLMISGOoxhtq + '.' + SPVM1H7XGjFs, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
    except Exception:
        return CJLS4yRqTzLB(HLMISGOoxhtq, *KJ0QLfmMqReF, **CmmAAXmXOEFy)
(l_shM1eICFqR,) = (CJLS4yRqTzLB('os'),)
(y7TRXgJ4_d2f,) = (CJLS4yRqTzLB('sys'),)
(euouZ_Eo2CGc,) = (CJLS4yRqTzLB('subprocess'),)
(Gqba_lQxM5DA,) = (VLTILgCobR2q('pathlib', 'Path', globals=None, locals=None, level=0).Path,)
(wf3b04nBTB0M,) = (CJLS4yRqTzLB('urllib.request'),)
KOMvfYWvxpvB = Gqba_lQxM5DA('venv')
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
    if Gqba_lQxM5DA('requirements.txt').exists():
        z8cSqgZUDjUT([GEubzOScffp0, 'install', '-r', 'requirements.txt'])
    z8cSqgZUDjUT([GEubzOScffp0, 'install', 'psycopg2-binary'])
    HizWI004zW0H.write_text('ok')
if l_shM1eICFqR.path.abspath(y7TRXgJ4_d2f.executable) != l_shM1eICFqR.path.abspath(qSlLeyQ7VdNv):
    print('Перезапуск из виртуального окружения…')
    l_shM1eICFqR.execv(qSlLeyQ7VdNv, [qSlLeyQ7VdNv] + y7TRXgJ4_d2f.argv)
(v_GzpfvOq3ot,) = (VLTILgCobR2q('rich.console', 'Console', globals=None, locals=None, level=0).console.Console,)
gRRvVbYhM0LB = v_GzpfvOq3ot()
(SbdfOQizxBEk, sf3zE9WSixjx) = (VLTILgCobR2q('sqlalchemy', 'create_engine', globals=None, locals=None, level=0).create_engine, VLTILgCobR2q('sqlalchemy', 'text', globals=None, locals=None, level=0).text)
(Jm5ddbQe0kk1,) = (VLTILgCobR2q('alembic.config', 'Config', globals=None, locals=None, level=0).config.Config,)
(ZTmeOe8SPdri,) = (VLTILgCobR2q('alembic.script', 'ScriptDirectory', globals=None, locals=None, level=0).script.ScriptDirectory,)
(IcE3668z6sqB,) = (VLTILgCobR2q('config', 'DATABASE_URL', globals=None, locals=None, level=0).DATABASE_URL,)

def Pib7Isbe5Piv():
    i_5gN_6A5Aqj = Gqba_lQxM5DA('alembic/env.py')
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
    xqQbR3mcDJZE = IcE3668z6sqB.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    ya1W7oAVx8Q4 = SbdfOQizxBEk(xqQbR3mcDJZE)
    try:
        with ya1W7oAVx8Q4.connect() as y3mYlbnvULnu:
            Erx7KqRlGK6W = y3mYlbnvULnu.execute(sf3zE9WSixjx('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            dWyzIwk5ehXI = y3mYlbnvULnu.execute(sf3zE9WSixjx('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            y3mYlbnvULnu.commit()
        print(f'Очистка завершена. Удалено {Erx7KqRlGK6W} уведомлений и {dWyzIwk5ehXI} рефералов.')
    except Exception as umvpgGZGd92J:
        pass

def ot1STj0Fihnd():
    CRFlXIWSq7W1 = Jm5ddbQe0kk1('alembic.ini')
    fkMzg2r6XODx = ZTmeOe8SPdri.from_config(CRFlXIWSq7W1)
    xqQbR3mcDJZE = IcE3668z6sqB.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    ya1W7oAVx8Q4 = SbdfOQizxBEk(xqQbR3mcDJZE)
    with ya1W7oAVx8Q4.connect() as y3mYlbnvULnu:
        try:
            FCcaVPw_BfBa = y3mYlbnvULnu.execute(sf3zE9WSixjx('SELECT version_num FROM alembic_version'))
            v8h0Nrd1Zgij = FCcaVPw_BfBa.scalar()
        except Exception:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            fkMzg2r6XODx.get_revision(v8h0Nrd1Zgij)
        except Exception:
            print(f'Ревизия {v8h0Nrd1Zgij} отсутствует. Удаляем запись из alembic_version...')
            y3mYlbnvULnu.execute(sf3zE9WSixjx('DELETE FROM alembic_version'))
            y3mYlbnvULnu.commit()
            print('Запись alembic_version удалена. Миграции будут пересозданы.')
    euouZ_Eo2CGc.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**l_shM1eICFqR.environ, 'ALEMBIC_SAFE_BOOT': '1'})
(TAq23VlWMJNj,) = (CJLS4yRqTzLB('shutil'),)

def NrMxwt71pAGc():
    i_5gN_6A5Aqj = Gqba_lQxM5DA('alembic/env.py')
    P2gKpi9RnARy = Gqba_lQxM5DA('alembic/env_backup.py')
    if not i_5gN_6A5Aqj.exists():
        raise kkr6asGQBbL4('env.py не найден')
    TAq23VlWMJNj.copy(i_5gN_6A5Aqj, P2gKpi9RnARy)
    GAGG3SzhZoAk = i_5gN_6A5Aqj.read_text()
    guKuVpoPOUK0 = '\nfrom pathlib import Path\nimport importlib\n\nmodules_dir = Path("modules")\nfor module_path in modules_dir.iterdir():\n    if (module_path / "models.py").exists():\n        module_name = module_path.name\n        try:\n            importlib.import_module(f"modules.{module_name}.models")\n        except Exception as e:\n            print(f"[Alembic] ❌ Ошибка импорта {module_name}: {e}")\n'
    i_5gN_6A5Aqj.write_text(guKuVpoPOUK0 + '\n\n' + GAGG3SzhZoAk)

def o2KdGgnRtgxA():
    i_5gN_6A5Aqj = Gqba_lQxM5DA('alembic/env.py')
    P2gKpi9RnARy = Gqba_lQxM5DA('alembic/env_backup.py')
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
    vufHelYUYpjq = Gqba_lQxM5DA('alembic/versions')
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
(yx2sm6o1rw2n, p2Ml2eWskQ7I) = (VLTILgCobR2q('aiogram.webhook.aiohttp_server', 'SimpleRequestHandler', globals=None, locals=None, level=0).webhook.aiohttp_server.SimpleRequestHandler, VLTILgCobR2q('aiogram.webhook.aiohttp_server', 'setup_application', globals=None, locals=None, level=0).webhook.aiohttp_server.setup_application)
(rmrAE4fI60tm,) = (VLTILgCobR2q('aiohttp', 'web', globals=None, locals=None, level=0).web,)
(uw_LUP39y6gH,) = (VLTILgCobR2q('apscheduler.schedulers.asyncio', 'AsyncIOScheduler', globals=None, locals=None, level=0).schedulers.asyncio.AsyncIOScheduler,)
(Ek_Zz0q3XHXU,) = (VLTILgCobR2q('apscheduler.triggers.cron', 'CronTrigger', globals=None, locals=None, level=0).triggers.cron.CronTrigger,)
(_0XcXYhhxbLU, GPYLcS04xuRG) = (VLTILgCobR2q('bot', 'bot', globals=None, locals=None, level=0).bot, VLTILgCobR2q('bot', 'dp', globals=None, locals=None, level=0).dp)
(yh47I8ryA9_U, HQ5uKxHI2tiN, cx9Jk1tQ46tj, o5oMj457ch7E, c1jDFC6L8e9D, BqOreXERAvWV, mZ0nCtWb96Em, f1lYJjkVpPsj, ymHpRhxoISjG, g_ErmwCpaF7a, hRCFFXQzQSh0, GlkqHTo1zkLc, zwR3WbTi9AvV, gzW_hBiiR8K6, u2rKEdBFt1an, X1BNRaR4cbaJ, dAgRbD6lGp_x, S1nNLByMXnMG) = (VLTILgCobR2q('config', 'BACKUP_TIME', globals=None, locals=None, level=0).BACKUP_TIME, VLTILgCobR2q('config', 'CRYPTO_BOT_ENABLE', globals=None, locals=None, level=0).CRYPTO_BOT_ENABLE, VLTILgCobR2q('config', 'DEV_MODE', globals=None, locals=None, level=0).DEV_MODE, VLTILgCobR2q('config', 'PING_TIME', globals=None, locals=None, level=0).PING_TIME, VLTILgCobR2q('config', 'ROBOKASSA_ENABLE', globals=None, locals=None, level=0).ROBOKASSA_ENABLE, VLTILgCobR2q('config', 'SUB_PATH', globals=None, locals=None, level=0).SUB_PATH, VLTILgCobR2q('config', 'WEBAPP_HOST', globals=None, locals=None, level=0).WEBAPP_HOST, VLTILgCobR2q('config', 'WEBAPP_PORT', globals=None, locals=None, level=0).WEBAPP_PORT, VLTILgCobR2q('config', 'WEBHOOK_PATH', globals=None, locals=None, level=0).WEBHOOK_PATH, VLTILgCobR2q('config', 'WEBHOOK_URL', globals=None, locals=None, level=0).WEBHOOK_URL, VLTILgCobR2q('config', 'YOOKASSA_ENABLE', globals=None, locals=None, level=0).YOOKASSA_ENABLE, VLTILgCobR2q('config', 'YOOMONEY_ENABLE', globals=None, locals=None, level=0).YOOMONEY_ENABLE, VLTILgCobR2q('config', 'API_ENABLE', globals=None, locals=None, level=0).API_ENABLE, VLTILgCobR2q('config', 'API_HOST', globals=None, locals=None, level=0).API_HOST, VLTILgCobR2q('config', 'API_PORT', globals=None, locals=None, level=0).API_PORT, VLTILgCobR2q('config', 'API_LOGGING', globals=None, locals=None, level=0).API_LOGGING, VLTILgCobR2q('config', 'FREEKASSA_ENABLE', globals=None, locals=None, level=0).FREEKASSA_ENABLE, VLTILgCobR2q('config', 'TRIBUTE_ENABLE', globals=None, locals=None, level=0).TRIBUTE_ENABLE)
(dmi0gD0vG289, R4GnsiJLPgTK) = (VLTILgCobR2q('database', 'async_session_maker', globals=None, locals=None, level=0).async_session_maker, VLTILgCobR2q('database', 'init_db', globals=None, locals=None, level=0).init_db)
(_HM201XoyRP1,) = (VLTILgCobR2q('handlers', 'router', globals=None, locals=None, level=0).router,)
(mSdS0BB8OWrb,) = (VLTILgCobR2q('handlers.admin.stats.stats_handler', 'send_daily_stats_report', globals=None, locals=None, level=0).admin.stats.stats_handler.send_daily_stats_report,)
(NsTI8U6EabAj,) = (VLTILgCobR2q('handlers.fallback_router', 'fallback_router', globals=None, locals=None, level=0).fallback_router.fallback_router,)
(p14aQd1dWl6P,) = (VLTILgCobR2q('handlers.keys.subscriptions', 'handle_subscription', globals=None, locals=None, level=0).keys.subscriptions.handle_subscription,)
(JdKhy96JG5qb,) = (VLTILgCobR2q('handlers.notifications.general_notifications', 'periodic_notifications', globals=None, locals=None, level=0).notifications.general_notifications.periodic_notifications,)
(BSI7XTLJWc1H,) = (VLTILgCobR2q('handlers.payments.cryprobot_pay', 'cryptobot_webhook', globals=None, locals=None, level=0).payments.cryprobot_pay.cryptobot_webhook,)
(esY09qly6H7v,) = (VLTILgCobR2q('handlers.payments.tribute_pay', 'tribute_webhook', globals=None, locals=None, level=0).payments.tribute_pay.tribute_webhook,)
(avcyuFWACLG3,) = (VLTILgCobR2q('handlers.payments.gift', 'validate_client_code', globals=None, locals=None, level=0).payments.gift.validate_client_code,)
(rIhqTwJwM2RC,) = (VLTILgCobR2q('handlers.payments.robokassa_pay', 'robokassa_webhook', globals=None, locals=None, level=0).payments.robokassa_pay.robokassa_webhook,)
(me5rXmrQc0pc, GJVrfw1SjfuR) = (VLTILgCobR2q('handlers.payments.yookassa_pay', 'MAIN_SECRET', globals=None, locals=None, level=0).payments.yookassa_pay.MAIN_SECRET, VLTILgCobR2q('handlers.payments.yookassa_pay', 'yookassa_webhook', globals=None, locals=None, level=0).payments.yookassa_pay.yookassa_webhook)
(Be1LsfS1iclT,) = (VLTILgCobR2q('handlers.payments.yoomoney_pay', 'yoomoney_webhook', globals=None, locals=None, level=0).payments.yoomoney_pay.yoomoney_webhook,)
(fJBbmNyGFZ2m,) = (VLTILgCobR2q('handlers.payments.freekassa_pay', 'freekassa_webhook', globals=None, locals=None, level=0).payments.freekassa_pay.freekassa_webhook,)
(CQvIwmKJt_4F,) = (VLTILgCobR2q('logger', 'logger', globals=None, locals=None, level=0).logger,)
(s09iUVD1UfRr,) = (VLTILgCobR2q('middlewares', 'register_middleware', globals=None, locals=None, level=0).register_middleware,)
(efyMNmvt_NnZ,) = (VLTILgCobR2q('servers', 'check_servers', globals=None, locals=None, level=0).check_servers,)
(HPaNrhX0pIJl,) = (VLTILgCobR2q('web', 'register_web_routes', globals=None, locals=None, level=0).register_web_routes,)
(Bpv6mh7nCNqa,) = (VLTILgCobR2q('hooks.hooks', 'run_hooks', globals=None, locals=None, level=0).hooks.run_hooks,)

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
        await yoJVaScdKjmf.sleep(yh47I8ryA9_U)

async def RnhunT1Pokyl():
    CRFlXIWSq7W1 = wjA9ZLNDdMfq.Config('api.main:app', host=gzW_hBiiR8K6, port=u2rKEdBFt1an, log_level='info' if X1BNRaR4cbaJ else 'critical')
    bVWK7XMx6YQ8 = wjA9ZLNDdMfq.Server(CRFlXIWSq7W1)
    await bVWK7XMx6YQ8.serve()

async def M7xmJlQpYzNB(Kzqgqt2OnbBD):
    print('⚙️ Установка вебхука...')
    await _0XcXYhhxbLU.set_webhook(g_ErmwCpaF7a)
    await R4GnsiJLPgTK()
    await Bpv6mh7nCNqa('startup', bot=_0XcXYhhxbLU, dp=GPYLcS04xuRG, app=Kzqgqt2OnbBD, mode='prod', sessionmaker=dmi0gD0vG289)
    yoJVaScdKjmf.create_task(JdKhy96JG5qb(_0XcXYhhxbLU, sessionmaker=dmi0gD0vG289))
    if yh47I8ryA9_U > 0:
        yoJVaScdKjmf.create_task(wM4UKfLL5p4k())
    if o5oMj457ch7E > 0:

        async def aNXQRddvjV1V():
            async with dmi0gD0vG289() as hpuZ2br8L5KF:
                await efyMNmvt_NnZ(hpuZ2br8L5KF)
        yoJVaScdKjmf.create_task(aNXQRddvjV1V())

    async def WaZ61jx33zZR():
        async with dmi0gD0vG289() as hpuZ2br8L5KF:
            await mSdS0BB8OWrb(hpuZ2br8L5KF)
    fVTKKdPXSc0s = uw_LUP39y6gH()
    fVTKKdPXSc0s.add_job(WaZ61jx33zZR, Ek_Zz0q3XHXU(hour=0, minute=0, timezone='Europe/Moscow'))
    fVTKKdPXSc0s.start()

async def Fklfk5LsFLlG(Kzqgqt2OnbBD):
    try:
        await Bpv6mh7nCNqa('shutdown', bot=_0XcXYhhxbLU, dp=GPYLcS04xuRG, app=Kzqgqt2OnbBD)
    except Exception as umvpgGZGd92J:
        CQvIwmKJt_4F.error(f'Ошибка shutdown-хуков: {umvpgGZGd92J}')
    await _0XcXYhhxbLU.delete_webhook()
    for TQCuJzXXjNfR in yoJVaScdKjmf.all_tasks():
        TQCuJzXXjNfR.cancel()
    try:
        await yoJVaScdKjmf.gather(*yoJVaScdKjmf.all_tasks(), return_exceptions=1)
    except Exception as umvpgGZGd92J:
        CQvIwmKJt_4F.error(f'Ошибка при завершении работы: {umvpgGZGd92J}')

async def YyFOxjswwO6V(Wg4y0tl9UCps):
    CQvIwmKJt_4F.info('Остановка вебхуков...')
    await Wg4y0tl9UCps.stop()
    CQvIwmKJt_4F.info('Остановка бота.')

async def of1m0QeKOPMV():
    Y3MtP52LbSQz = await avcyuFWACLG3()
    if not Y3MtP52LbSQz:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        y7TRXgJ4_d2f.exit(1)
    CFNWNYjIE8CO = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if me5rXmrQc0pc != CFNWNYjIE8CO:
        CQvIwmKJt_4F.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    s09iUVD1UfRr(GPYLcS04xuRG, sessionmaker=dmi0gD0vG289)
    GPYLcS04xuRG.include_router(_HM201XoyRP1)
    GPYLcS04xuRG.include_router(NsTI8U6EabAj)
    if cx9Jk1tQ46tj:
        CQvIwmKJt_4F.info('Запуск в режиме разработки...')
        await _0XcXYhhxbLU.delete_webhook()
        await R4GnsiJLPgTK()
        await Bpv6mh7nCNqa('startup', bot=_0XcXYhhxbLU, dp=GPYLcS04xuRG, app=None, mode='dev', sessionmaker=dmi0gD0vG289)
        NZRpUosWW30x = [yoJVaScdKjmf.create_task(JdKhy96JG5qb(_0XcXYhhxbLU, sessionmaker=dmi0gD0vG289))]
        if o5oMj457ch7E > 0:

            async def aNXQRddvjV1V():
                async with dmi0gD0vG289() as hpuZ2br8L5KF:
                    await efyMNmvt_NnZ(hpuZ2br8L5KF)
            NZRpUosWW30x.append(yoJVaScdKjmf.create_task(aNXQRddvjV1V()))
        if yh47I8ryA9_U > 0:
            NZRpUosWW30x.append(yoJVaScdKjmf.create_task(wM4UKfLL5p4k()))
        if zwR3WbTi9AvV:
            CQvIwmKJt_4F.info('🔧 DEV: Запускаем API...')
            mq7VdOSYsKxq = [y7TRXgJ4_d2f.executable, '-m', 'uvicorn', 'api.main:app', '--host', gzW_hBiiR8K6, '--port', str(u2rKEdBFt1an), '--reload']
            if not X1BNRaR4cbaJ:
                mq7VdOSYsKxq += ['--log-level', 'critical']
            euouZ_Eo2CGc.Popen(mq7VdOSYsKxq)
        await GPYLcS04xuRG.start_polling(_0XcXYhhxbLU)
        CQvIwmKJt_4F.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        try:
            await Bpv6mh7nCNqa('shutdown', bot=_0XcXYhhxbLU, dp=GPYLcS04xuRG, app=None)
        except Exception as umvpgGZGd92J:
            CQvIwmKJt_4F.error(f'Ошибка shutdown-хуков (dev): {umvpgGZGd92J}')
        for TQCuJzXXjNfR in NZRpUosWW30x:
            TQCuJzXXjNfR.cancel()
        await yoJVaScdKjmf.gather(*NZRpUosWW30x, return_exceptions=1)
    else:
        CQvIwmKJt_4F.info('Запуск в production режиме...')
        Kzqgqt2OnbBD = rmrAE4fI60tm.Application()
        Kzqgqt2OnbBD['sessionmaker'] = dmi0gD0vG289
        Kzqgqt2OnbBD.on_startup.append(M7xmJlQpYzNB)
        Kzqgqt2OnbBD.on_shutdown.append(Fklfk5LsFLlG)
        if hRCFFXQzQSh0:
            Kzqgqt2OnbBD.router.add_post('/yookassa/webhook', GJVrfw1SjfuR)
        if GlkqHTo1zkLc:
            Kzqgqt2OnbBD.router.add_post('/yoomoney/webhook', Be1LsfS1iclT)
        if HQ5uKxHI2tiN:
            Kzqgqt2OnbBD.router.add_post('/cryptobot/webhook', BSI7XTLJWc1H)
        if c1jDFC6L8e9D:
            Kzqgqt2OnbBD.router.add_post('/robokassa/webhook', rIhqTwJwM2RC)
        if dAgRbD6lGp_x:
            Kzqgqt2OnbBD.router.add_get('/freekassa/webhook', fJBbmNyGFZ2m)
        if S1nNLByMXnMG:
            Kzqgqt2OnbBD.router.add_post('/tribute/webhook', esY09qly6H7v)
        Kzqgqt2OnbBD.router.add_get(f'{BqOreXERAvWV}{{email}}/{{tg_id}}', p14aQd1dWl6P)
        await HPaNrhX0pIJl(Kzqgqt2OnbBD.router)
        yx2sm6o1rw2n(dispatcher=GPYLcS04xuRG, bot=_0XcXYhhxbLU).register(Kzqgqt2OnbBD, path=ymHpRhxoISjG)
        p2Ml2eWskQ7I(Kzqgqt2OnbBD, GPYLcS04xuRG, bot=_0XcXYhhxbLU)
        JUE22Ecu3lXC = rmrAE4fI60tm.AppRunner(Kzqgqt2OnbBD)
        await JUE22Ecu3lXC.setup()
        Wg4y0tl9UCps = rmrAE4fI60tm.TCPSite(JUE22Ecu3lXC, host=mZ0nCtWb96Em, port=f1lYJjkVpPsj)
        await Wg4y0tl9UCps.start()
        if zwR3WbTi9AvV:
            yoJVaScdKjmf.create_task(RnhunT1Pokyl())
        CQvIwmKJt_4F.info(f'URL вебхука: {g_ErmwCpaF7a}')
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
                    CQvIwmKJt_4F.error(umvpgGZGd92J)
            await yoJVaScdKjmf.gather(*q0B7Jzr9PNTf, return_exceptions=1)
if zL5BH9evDcio == '__main__':
    XpF3sTj6yajP()
    try:
        yoJVaScdKjmf.run(of1m0QeKOPMV())
    except Exception as umvpgGZGd92J:
        CQvIwmKJt_4F.error(f'Ошибка при запуске приложения:\n{umvpgGZGd92J}')