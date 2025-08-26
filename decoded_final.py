import importlib

def TKizvQ0BnfYh(lVOb8D0b52U0, oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE):
    try:
        return importlib.import_module(lVOb8D0b52U0 + importlib.import_module('.')('utf-8') + oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
    except Exception:
        return importlib.import_module(lVOb8D0b52U0, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
(FyYEeTFyaEwm,) = (importlib.import_module(importlib.import_module('os')('utf-8')),)
(UhKVW6ci2ufp,) = (importlib.import_module(importlib.import_module('subprocess')('utf-8')),)
(NlMf_Ll9d9TE,) = (importlib.import_module(importlib.import_module('sys')('utf-8')),)
(iZQnRId6lk4a,) = (getattr(TKizvQ0BnfYh(importlib.import_module('pathlib')('utf-8'), importlib.import_module('Path')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('Path')('utf-8')),)
if not getattr(FyYEeTFyaEwm.path, importlib.import_module('exists')('utf-8'))(importlib.import_module('venv')('utf-8')):
    print(importlib.import_module('Создание виртуального окружения...')('utf-8'))
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([getattr(NlMf_Ll9d9TE, importlib.import_module('executable')('utf-8')), importlib.import_module('-m')('utf-8'), importlib.import_module('venv')('utf-8'), importlib.import_module('venv')('utf-8')], check=1)
venv_python = FyYEeTFyaEwm.path.abspath(importlib.import_module('venv/bin/python')('utf-8'))
if getattr(NlMf_Ll9d9TE, importlib.import_module('executable')('utf-8')) != venv_python:
    print(importlib.import_module('Перезапуск из виртуального окружения...')('utf-8'))
    getattr(FyYEeTFyaEwm, importlib.import_module('execv')('utf-8'))(venv_python, [venv_python] + getattr(NlMf_Ll9d9TE, importlib.import_module('argv')('utf-8')))
venv_marker = FyYEeTFyaEwm.path.join(importlib.import_module('venv')('utf-8'), importlib.import_module('.installed')('utf-8'))
if not getattr(FyYEeTFyaEwm.path, importlib.import_module('exists')('utf-8'))(venv_marker):
    print(importlib.import_module('Установка зависимостей...')('utf-8'))
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([importlib.import_module('venv/bin/pip')('utf-8'), importlib.import_module('install')('utf-8'), importlib.import_module('--upgrade')('utf-8'), importlib.import_module('pip')('utf-8')], check=1)
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([importlib.import_module('venv/bin/pip')('utf-8'), importlib.import_module('install')('utf-8'), importlib.import_module('-r')('utf-8'), importlib.import_module('requirements.txt')('utf-8')], check=1)
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([importlib.import_module('venv/bin/pip')('utf-8'), importlib.import_module('install')('utf-8'), importlib.import_module('psycopg2-binary')('utf-8')], check=1)
    getattr(iZQnRId6lk4a(venv_marker), importlib.import_module('write_text')('utf-8'))(importlib.import_module('ok')('utf-8'))

def init_alembic():
    alembic_env_path = iZQnRId6lk4a(importlib.import_module('alembic/env.py')('utf-8'))
    if getattr(alembic_env_path, importlib.import_module('exists')('utf-8'))():
        print(importlib.import_module('ℹAlembic уже инициализирован.')('utf-8'))
        return
    print(importlib.import_module('🛠️ Инициализация Alembic...')('utf-8'))
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([importlib.import_module('venv/bin/alembic')('utf-8'), importlib.import_module('init')('utf-8'), importlib.import_module('alembic')('utf-8')], check=1)
    if getattr(alembic_env_path, importlib.import_module('exists')('utf-8'))():
        CRcKJ5Z0I1XF = alembic_env_path.read_text()
        alembic_env_patch = importlib.import_module('from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata')('utf-8')
        CRcKJ5Z0I1XF = CRcKJ5Z0I1XF.replace(importlib.import_module('target_metadata = None')('utf-8'), alembic_env_patch)
        getattr(alembic_env_path, importlib.import_module('write_text')('utf-8'))(CRcKJ5Z0I1XF)
    print(importlib.import_module('✅ Alembic инициализирован.')('utf-8'))
(Q7tClP07Cr24, CRcKJ5Z0I1XF) = (getattr(TKizvQ0BnfYh(importlib.import_module('sqlalchemy')('utf-8'), importlib.import_module('create_engine')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('create_engine')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('sqlalchemy')('utf-8'), importlib.import_module('text')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('text')('utf-8')))
(kYsphmT4sjV8,) = (getattr(getattr(TKizvQ0BnfYh(importlib.import_module('alembic.config')('utf-8'), importlib.import_module('Config')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('config')('utf-8')), importlib.import_module('Config')('utf-8')),)
(bX0dgRLufyU9,) = (getattr(getattr(TKizvQ0BnfYh(importlib.import_module('alembic.script')('utf-8'), importlib.import_module('ScriptDirectory')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('script')('utf-8')), importlib.import_module('ScriptDirectory')('utf-8')),)
(etiivloU5GNO,) = (getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('DATABASE_URL')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('DATABASE_URL')('utf-8')),)

def cleanup_orphans():
    print(importlib.import_module('🧹 Очистка висячих ссылок перед миграциями...')('utf-8'))
    sync_db_url = etiivloU5GNO.replace(importlib.import_module('postgresql+asyncpg')('utf-8'), importlib.import_module('postgresql+psycopg2')('utf-8'))
    engine = Q7tClP07Cr24(sync_db_url)
    try:
        with getattr(engine, importlib.import_module('connect')('utf-8'))() as conn:
            deleted_notifications = conn.execute(CRcKJ5Z0I1XF(importlib.import_module('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')('utf-8'))).rowcount
            deleted_referrals = conn.execute(CRcKJ5Z0I1XF(importlib.import_module('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')('utf-8'))).rowcount
            getattr(conn, importlib.import_module('commit')('utf-8'))()
        print(f'✅ Очистка завершена. Удалено {deleted_notifications} уведомлений и {deleted_referrals} рефералов.')
    except Exception as exc:
        print(f'⚠️ Ошибка при очистке висячих ссылок: {exc}')

def fix_broken_revision():
    NruZidUcKdMe = kYsphmT4sjV8(importlib.import_module('alembic.ini')('utf-8'))
    script_dir = bX0dgRLufyU9.from_config(NruZidUcKdMe)
    sync_db_url = etiivloU5GNO.replace(importlib.import_module('postgresql+asyncpg')('utf-8'), importlib.import_module('postgresql+psycopg2')('utf-8'))
    engine = Q7tClP07Cr24(sync_db_url)
    with getattr(engine, importlib.import_module('connect')('utf-8'))() as conn:
        try:
            result = conn.execute(CRcKJ5Z0I1XF(importlib.import_module('SELECT version_num FROM alembic_version')('utf-8')))
            revision_id = result.scalar()
        except Exception:
            print(importlib.import_module('ℹТаблица alembic_version не найдена — пропускаем проверку.')('utf-8'))
            return
        try:
            getattr(script_dir, importlib.import_module('get_revision')('utf-8'))(revision_id)
        except Exception:
            print(f'Ревизия {revision_id} отсутствует. Удаляем запись из alembic_version...')
            getattr(conn, importlib.import_module('execute')('utf-8'))(CRcKJ5Z0I1XF(importlib.import_module('DELETE FROM alembic_version')('utf-8')))
            getattr(conn, importlib.import_module('commit')('utf-8'))()
    print(importlib.import_module('Удалена повреждённая ревизия. Выполняем stamp head...')('utf-8'))
    getattr(UhKVW6ci2ufp, importlib.import_module('run')('utf-8'))([importlib.import_module('venv/bin/alembic')('utf-8'), importlib.import_module('stamp')('utf-8'), importlib.import_module('head')('utf-8')], check=1, env={**getattr(FyYEeTFyaEwm, importlib.import_module('environ')('utf-8')), importlib.import_module('ALEMBIC_SAFE_BOOT')('utf-8'): importlib.import_module('1')('utf-8')})

def generate_and_apply_migrations():
    print(importlib.import_module('Генерация и применение миграций...')('utf-8'))
    cleanup_orphans()
    fix_broken_revision()
    result = UhKVW6ci2ufp.run([importlib.import_module('venv/bin/alembic')('utf-8'), importlib.import_module('revision')('utf-8'), importlib.import_module('--autogenerate')('utf-8'), importlib.import_module('-m')('utf-8'), importlib.import_module('Auto migration')('utf-8')], capture_output=1, text=1)
    if importlib.import_module('No changes in schema detected')('utf-8') in getattr(result, importlib.import_module('stdout')('utf-8')):
        print(importlib.import_module('ℹИзменений в моделях нет — миграция не требуется.')('utf-8'))
    else:
        print(importlib.import_module('Миграция создана. Применяем...')('utf-8'))
        Hvn5kk0_vFwt = UhKVW6ci2ufp.run([importlib.import_module('venv/bin/alembic')('utf-8'), importlib.import_module('upgrade')('utf-8'), importlib.import_module('head')('utf-8')], capture_output=1, text=1)
        if getattr(Hvn5kk0_vFwt, importlib.import_module('returncode')('utf-8')) != 0:
            print(importlib.import_module('❌ Ошибка при применении миграции:')('utf-8'))
            print(importlib.import_module('STDOUT:')('utf-8'))
            print(getattr(Hvn5kk0_vFwt, importlib.import_module('stdout')('utf-8')))
            print(importlib.import_module('STDERR:')('utf-8'))
            print(getattr(Hvn5kk0_vFwt, importlib.import_module('stderr')('utf-8')))
            getattr(NlMf_Ll9d9TE, importlib.import_module('exit')('utf-8'))(1)
        print(importlib.import_module('✅ Alembic upgrade успешно выполнен.')('utf-8'))

def ensure_migrations():
    init_alembic()
    sLMMm8FcjIhp = iZQnRId6lk4a(importlib.import_module('alembic/versions')('utf-8'))
    if not getattr(sLMMm8FcjIhp, importlib.import_module('exists')('utf-8'))():
        getattr(sLMMm8FcjIhp, importlib.import_module('mkdir')('utf-8'))(parents=1)
    generate_and_apply_migrations()
ensure_migrations()
(IgbbC5J5z2tZ,) = (importlib.import_module(importlib.import_module('asyncio')('utf-8')),)
(FyYEeTFyaEwm,) = (importlib.import_module(importlib.import_module('os')('utf-8')),)
(d29IHszvBPJN,) = (importlib.import_module(importlib.import_module('signal')('utf-8')),)
(UhKVW6ci2ufp,) = (importlib.import_module(importlib.import_module('subprocess')('utf-8')),)
(NlMf_Ll9d9TE,) = (importlib.import_module(importlib.import_module('sys')('utf-8')),)
(c5NNV3V3Ry3y,) = (importlib.import_module(importlib.import_module('uvicorn')('utf-8')),)
(dJnsTNALuDBU, dck_6UV5RWy6) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('aiogram.webhook.aiohttp_server')('utf-8'), importlib.import_module('SimpleRequestHandler')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('webhook')('utf-8')), importlib.import_module('aiohttp_server')('utf-8')), importlib.import_module('SimpleRequestHandler')('utf-8')), getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('aiogram.webhook.aiohttp_server')('utf-8'), importlib.import_module('setup_application')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('webhook')('utf-8')), importlib.import_module('aiohttp_server')('utf-8')), importlib.import_module('setup_application')('utf-8')))
(S16nYXJrI_8a,) = (getattr(TKizvQ0BnfYh(importlib.import_module('aiohttp')('utf-8'), importlib.import_module('web')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('web')('utf-8')),)
(dmkLf2NsdNqg,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('apscheduler.schedulers.asyncio')('utf-8'), importlib.import_module('AsyncIOScheduler')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('schedulers')('utf-8')), importlib.import_module('asyncio')('utf-8')), importlib.import_module('AsyncIOScheduler')('utf-8')),)
(CtAaFtUYmGm7,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('apscheduler.triggers.cron')('utf-8'), importlib.import_module('CronTrigger')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('triggers')('utf-8')), importlib.import_module('cron')('utf-8')), importlib.import_module('CronTrigger')('utf-8')),)
(LY5TOgVHXSy5,) = (getattr(TKizvQ0BnfYh(importlib.import_module('backup')('utf-8'), importlib.import_module('backup_database')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('backup_database')('utf-8')),)
(B1br9W7_bn2X, QawnGHulCbas) = (getattr(TKizvQ0BnfYh(importlib.import_module('bot')('utf-8'), importlib.import_module('bot')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('bot')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('bot')('utf-8'), importlib.import_module('dp')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('dp')('utf-8')))
(cOhAqchD95fm, gXLBwYTBCUt7, QH1oQYKrN7qd, DikaXCEDxTz2, hMtGAoAJKuQm, SUB_PATH, iA9Ziao7fn9P, CU6sEfk1r5mF, n7zYTnBpvjmO, WEBHOOK_URL, yP2r9gf4oG8a, xHfEv2FKkJDn, Nuk8G57TsVme, YKUElrdccEwu, vIr_pqkFXy3z, K9_RuISjrOaT, Q51yqS3LP9Ft) = (getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('BACKUP_TIME')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('BACKUP_TIME')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('CRYPTO_BOT_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('CRYPTO_BOT_ENABLE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('DEV_MODE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('DEV_MODE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('PING_TIME')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('PING_TIME')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('ROBOKASSA_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('ROBOKASSA_ENABLE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('SUB_PATH')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('SUB_PATH')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('WEBAPP_HOST')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('WEBAPP_HOST')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('WEBAPP_PORT')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('WEBAPP_PORT')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('WEBHOOK_PATH')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('WEBHOOK_PATH')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('WEBHOOK_URL')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('WEBHOOK_URL')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('YOOKASSA_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('YOOKASSA_ENABLE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('YOOMONEY_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('YOOMONEY_ENABLE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('API_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('API_ENABLE')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('API_HOST')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('API_HOST')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('API_PORT')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('API_PORT')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('API_LOGGING')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('API_LOGGING')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('config')('utf-8'), importlib.import_module('FREEKASSA_ENABLE')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('FREEKASSA_ENABLE')('utf-8')))
(cUt_1v7BqmdG, Q0676_Ys6MDk) = (getattr(TKizvQ0BnfYh(importlib.import_module('database')('utf-8'), importlib.import_module('async_session_maker')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('async_session_maker')('utf-8')), getattr(TKizvQ0BnfYh(importlib.import_module('database')('utf-8'), importlib.import_module('init_db')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('init_db')('utf-8')))
(Nnx4UIsVD5DW,) = (getattr(TKizvQ0BnfYh(importlib.import_module('handlers')('utf-8'), importlib.import_module('router')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('router')('utf-8')),)
(Nl3wzY0MRxUb,) = (getattr(getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.admin.stats.stats_handler')('utf-8'), importlib.import_module('send_daily_stats_report')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('admin')('utf-8')), importlib.import_module('stats')('utf-8')), importlib.import_module('stats_handler')('utf-8')), importlib.import_module('send_daily_stats_report')('utf-8')),)
(Lj61wtQvyyYG,) = (getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.fallback_router')('utf-8'), importlib.import_module('fallback_router')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('fallback_router')('utf-8')), importlib.import_module('fallback_router')('utf-8')),)
(_QMVLJZw6AAl,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.keys.subscriptions')('utf-8'), importlib.import_module('handle_subscription')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('keys')('utf-8')), importlib.import_module('subscriptions')('utf-8')), importlib.import_module('handle_subscription')('utf-8')),)
(w0n_fSKiXLno,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.notifications.general_notifications')('utf-8'), importlib.import_module('periodic_notifications')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('notifications')('utf-8')), importlib.import_module('general_notifications')('utf-8')), importlib.import_module('periodic_notifications')('utf-8')),)
(BI8caSrsEQLn,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.cryprobot_pay')('utf-8'), importlib.import_module('cryptobot_webhook')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('cryprobot_pay')('utf-8')), importlib.import_module('cryptobot_webhook')('utf-8')),)
(fTh9BL4qlePy,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.gift')('utf-8'), importlib.import_module('validate_client_code')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('gift')('utf-8')), importlib.import_module('validate_client_code')('utf-8')),)
(YIDxn0At0JLm,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.robokassa_pay')('utf-8'), importlib.import_module('robokassa_webhook')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('robokassa_pay')('utf-8')), importlib.import_module('robokassa_webhook')('utf-8')),)
(zHROqa7Vv7S4, yQcDOUG0lwO3) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.yookassa_pay')('utf-8'), importlib.import_module('MAIN_SECRET')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('yookassa_pay')('utf-8')), importlib.import_module('MAIN_SECRET')('utf-8')), getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.yookassa_pay')('utf-8'), importlib.import_module('yookassa_webhook')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('yookassa_pay')('utf-8')), importlib.import_module('yookassa_webhook')('utf-8')))
(CysYC_WVi6QN,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.yoomoney_pay')('utf-8'), importlib.import_module('yoomoney_webhook')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('yoomoney_pay')('utf-8')), importlib.import_module('yoomoney_webhook')('utf-8')),)
(CWTIC90Zi1Jk,) = (getattr(getattr(getattr(TKizvQ0BnfYh(importlib.import_module('handlers.payments.freekassa_pay')('utf-8'), importlib.import_module('freekassa_webhook')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('payments')('utf-8')), importlib.import_module('freekassa_pay')('utf-8')), importlib.import_module('freekassa_webhook')('utf-8')),)
(NoBTrJ0QkTMy,) = (getattr(TKizvQ0BnfYh(importlib.import_module('logger')('utf-8'), importlib.import_module('logger')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('logger')('utf-8')),)
(lrMgLENzItNN,) = (getattr(TKizvQ0BnfYh(importlib.import_module('middlewares')('utf-8'), importlib.import_module('register_middleware')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('register_middleware')('utf-8')),)
(KI__IpMinSme,) = (getattr(TKizvQ0BnfYh(importlib.import_module('servers')('utf-8'), importlib.import_module('check_servers')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('check_servers')('utf-8')),)
(vuUwn1WIpDH1,) = (getattr(TKizvQ0BnfYh(importlib.import_module('web')('utf-8'), importlib.import_module('register_web_routes')('utf-8'), globals=None, locals=None, level=0), importlib.import_module('register_web_routes')('utf-8')),)

def install_cli():
    (bIHNKSXd0ieD,) = (importlib.import_module(importlib.import_module('hashlib')('utf-8')),)
    launcher_path = FyYEeTFyaEwm.path.abspath(importlib.import_module('cli_launcher.py')('utf-8'))
    python_executable = NlMf_Ll9d9TE.executable
    bin_candidates = [importlib.import_module('/usr/local/bin')('utf-8'), importlib.import_module('/usr/bin')('utf-8'), FyYEeTFyaEwm.path.expanduser(importlib.import_module('~/.local/bin')('utf-8'))]
    for bin_dir in bin_candidates:
        if getattr(FyYEeTFyaEwm.path, importlib.import_module('isdir')('utf-8'))(bin_dir) and getattr(FyYEeTFyaEwm, importlib.import_module('access')('utf-8'))(bin_dir, getattr(FyYEeTFyaEwm, importlib.import_module('W_OK')('utf-8'))):
            break
    else:
        print(importlib.import_module('❌ Не удалось найти подходящий каталог для установки команды.')('utf-8'))
        return
    default_cmd = importlib.import_module('solobot')('utf-8')
    cmd_name = default_cmd
    cmd_path = FyYEeTFyaEwm.path.join(bin_dir, cmd_name)
    if getattr(FyYEeTFyaEwm.path, importlib.import_module('exists')('utf-8'))(cmd_path):
        try:
            with open(cmd_path, importlib.import_module('r')('utf-8')) as fh:
                existing_cmd = fh.read()
            if launcher_path in existing_cmd:
                return
            else:
                print(f'⚠️ Команда `{cmd_name}` уже установлена, но для другой копии бота.')
                new_cmd_name = input(importlib.import_module('Введите другое имя команды (например, solobot-test): ')('utf-8')).strip()
                if not new_cmd_name:
                    print(importlib.import_module('❌ Имя не указано. Пропускаем установку.')('utf-8'))
                    return
                cmd_name = new_cmd_name
                cmd_path = FyYEeTFyaEwm.path.join(bin_dir, cmd_name)
                if getattr(FyYEeTFyaEwm.path, importlib.import_module('exists')('utf-8'))(cmd_path):
                    print(f'❌ Команда `{cmd_name}` уже существует. Установка прервана.')
                    return
        except Exception as exc:
            print(f'⚠️ Ошибка при чтении команды {cmd_name}: {exc}')
            return
    try:
        with open(cmd_path, importlib.import_module('w')('utf-8')) as fh:
            getattr(fh, importlib.import_module('write')('utf-8'))(f"""#!/bin/bash\n'{python_executable}' '{launcher_path}' "$@"\n""")
        getattr(FyYEeTFyaEwm, importlib.import_module('chmod')('utf-8'))(cmd_path, 493)
        print(f'✅ Команда `{cmd_name}` установлена! Используйте: {cmd_name}')
    except Exception as exc:
        print(f'❌ Ошибка установки команды {cmd_name}: {exc}')

async def backup_loop():
    while True:
        await LY5TOgVHXSy5()
        await getattr(IgbbC5J5z2tZ, importlib.import_module('sleep')('utf-8'))(cOhAqchD95fm)

async def serve_api():
    NruZidUcKdMe = c5NNV3V3Ry3y.Config(importlib.import_module('api.main:app')('utf-8'), host=YKUElrdccEwu, port=vIr_pqkFXy3z, log_level=importlib.import_module('info')('utf-8') if K9_RuISjrOaT else importlib.import_module('critical')('utf-8'))
    server = c5NNV3V3Ry3y.Server(NruZidUcKdMe)
    await getattr(server, importlib.import_module('serve')('utf-8'))()

async def on_startup(dhwwiGt3_ntG):
    print(importlib.import_module('⚙️ Установка вебхука...')('utf-8'))
    await getattr(B1br9W7_bn2X, importlib.import_module('set_webhook')('utf-8'))(WEBHOOK_URL)
    await Q0676_Ys6MDk()
    getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(w0n_fSKiXLno(B1br9W7_bn2X, sessionmaker=cUt_1v7BqmdG))
    if cOhAqchD95fm > 0:
        getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(backup_loop())
    if DikaXCEDxTz2 > 0:

        async def run_check_servers():
            async with cUt_1v7BqmdG() as session:
                await KI__IpMinSme(session)
        getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(run_check_servers())

    async def send_stats_job():
        async with cUt_1v7BqmdG() as session:
            await Nl3wzY0MRxUb(session)
    scheduler = dmkLf2NsdNqg()
    getattr(scheduler, importlib.import_module('add_job')('utf-8'))(send_stats_job, CtAaFtUYmGm7(hour=0, minute=0, timezone=importlib.import_module('Europe/Moscow')('utf-8')))
    getattr(scheduler, importlib.import_module('start')('utf-8'))()
    print(importlib.import_module('✅ on_startup завершён.')('utf-8'))

async def on_shutdown(dhwwiGt3_ntG):
    await getattr(B1br9W7_bn2X, importlib.import_module('delete_webhook')('utf-8'))()
    for task in getattr(IgbbC5J5z2tZ, importlib.import_module('all_tasks')('utf-8'))():
        getattr(task, importlib.import_module('cancel')('utf-8'))()
    try:
        await getattr(IgbbC5J5z2tZ, importlib.import_module('gather')('utf-8'))(*getattr(IgbbC5J5z2tZ, importlib.import_module('all_tasks')('utf-8'))(), return_exceptions=1)
    except Exception as exc:
        getattr(NoBTrJ0QkTMy, importlib.import_module('error')('utf-8'))(f'Ошибка при завершении работы: {exc}')

async def iCccCTUyxALg(PGcAj_zEi4a3):
    getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('Остановка вебхуков...')('utf-8'))
    await getattr(site, importlib.import_module('stop')('utf-8'))()
    getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('Остановка бота.')('utf-8'))

async def main():
    bZnyVT5QtFH6 = await fTh9BL4qlePy()
    if not bZnyVT5QtFH6:
        print(importlib.import_module('❌ Бот не активирован. Проверьте ваш клиентский код.')('utf-8'))
        getattr(NlMf_Ll9d9TE, importlib.import_module('exit')('utf-8'))(1)
    DAfvdd0x1Xo6 = importlib.import_module('SOLO-ACCESS-KEY-B4TN-92QX-L7ME')('utf-8')
    if zHROqa7Vv7S4 != DAfvdd0x1Xo6:
        getattr(NoBTrJ0QkTMy, importlib.import_module('error')('utf-8'))(importlib.import_module('Нарушена целостность файлов! Обновитесь с полной заменой папки!')('utf-8'))
        return
    lrMgLENzItNN(QawnGHulCbas, sessionmaker=cUt_1v7BqmdG)
    getattr(QawnGHulCbas, importlib.import_module('include_router')('utf-8'))(Nnx4UIsVD5DW)
    getattr(QawnGHulCbas, importlib.import_module('include_router')('utf-8'))(Lj61wtQvyyYG)
    if QH1oQYKrN7qd:
        getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('Запуск в режиме разработки...')('utf-8'))
        await getattr(B1br9W7_bn2X, importlib.import_module('delete_webhook')('utf-8'))()
        await Q0676_Ys6MDk()
        ktzqDrWNa2rM = [IgbbC5J5z2tZ.create_task(w0n_fSKiXLno(B1br9W7_bn2X, sessionmaker=cUt_1v7BqmdG))]
        if DikaXCEDxTz2 > 0:

            async def run_check_servers():
                async with cUt_1v7BqmdG() as session:
                    await KI__IpMinSme(session)
            getattr(ktzqDrWNa2rM, importlib.import_module('append')('utf-8'))(getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(run_check_servers()))
        if cOhAqchD95fm > 0:
            getattr(ktzqDrWNa2rM, importlib.import_module('append')('utf-8'))(getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(backup_loop()))
        if Nuk8G57TsVme:
            getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('🔧 DEV: Запускаем API...')('utf-8'))
            cmd = [NlMf_Ll9d9TE.executable, importlib.import_module('-m')('utf-8'), importlib.import_module('uvicorn')('utf-8'), importlib.import_module('api.main:app')('utf-8'), importlib.import_module('--host')('utf-8'), YKUElrdccEwu, importlib.import_module('--port')('utf-8'), str(vIr_pqkFXy3z), importlib.import_module('--reload')('utf-8')]
            if not K9_RuISjrOaT:
                cmd += [importlib.import_module('--log-level')('utf-8'), importlib.import_module('critical')('utf-8')]
            getattr(UhKVW6ci2ufp, importlib.import_module('Popen')('utf-8'))(cmd)
        await getattr(QawnGHulCbas, importlib.import_module('start_polling')('utf-8'))(B1br9W7_bn2X)
        getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('Polling остановлен в режиме разработки. Отмена фоновых задач...')('utf-8'))
        for task in ktzqDrWNa2rM:
            getattr(task, importlib.import_module('cancel')('utf-8'))()
        await getattr(IgbbC5J5z2tZ, importlib.import_module('gather')('utf-8'))(*ktzqDrWNa2rM, return_exceptions=1)
    else:
        getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(importlib.import_module('Запуск в production режиме...')('utf-8'))
        app = S16nYXJrI_8a.Application()
        app[importlib.import_module('sessionmaker')('utf-8')] = cUt_1v7BqmdG
        getattr(app.on_startup, importlib.import_module('append')('utf-8'))(on_startup)
        getattr(app.on_shutdown, importlib.import_module('append')('utf-8'))(on_shutdown)
        if yP2r9gf4oG8a:
            getattr(app.router, importlib.import_module('add_post')('utf-8'))(importlib.import_module('/yookassa/webhook')('utf-8'), yQcDOUG0lwO3)
        if xHfEv2FKkJDn:
            getattr(app.router, importlib.import_module('add_post')('utf-8'))(importlib.import_module('/yoomoney/webhook')('utf-8'), CysYC_WVi6QN)
        if gXLBwYTBCUt7:
            getattr(app.router, importlib.import_module('add_post')('utf-8'))(importlib.import_module('/cryptobot/webhook')('utf-8'), BI8caSrsEQLn)
        if hMtGAoAJKuQm:
            getattr(app.router, importlib.import_module('add_post')('utf-8'))(importlib.import_module('/robokassa/webhook')('utf-8'), YIDxn0At0JLm)
        if Q51yqS3LP9Ft:
            getattr(app.router, importlib.import_module('add_get')('utf-8'))(importlib.import_module('/freekassa/webhook')('utf-8'), CWTIC90Zi1Jk)
        getattr(app.router, importlib.import_module('add_get')('utf-8'))(f'{SUB_PATH}{{email}}/{{tg_id}}', _QMVLJZw6AAl)
        await vuUwn1WIpDH1(getattr(app, importlib.import_module('router')('utf-8')))
        getattr(dJnsTNALuDBU(dispatcher=QawnGHulCbas, bot=B1br9W7_bn2X), importlib.import_module('register')('utf-8'))(app, path=n7zYTnBpvjmO)
        dck_6UV5RWy6(app, QawnGHulCbas, bot=B1br9W7_bn2X)
        runner = S16nYXJrI_8a.AppRunner(app)
        await getattr(runner, importlib.import_module('setup')('utf-8'))()
        site = S16nYXJrI_8a.TCPSite(runner, host=iA9Ziao7fn9P, port=CU6sEfk1r5mF)
        await getattr(site, importlib.import_module('start')('utf-8'))()
        if Nuk8G57TsVme:
            getattr(IgbbC5J5z2tZ, importlib.import_module('create_task')('utf-8'))(serve_api())
        getattr(NoBTrJ0QkTMy, importlib.import_module('info')('utf-8'))(f'URL вебхука: {WEBHOOK_URL}')
        stop_event = IgbbC5J5z2tZ.Event()
        loop = IgbbC5J5z2tZ.get_event_loop()
        for sig in (getattr(d29IHszvBPJN, importlib.import_module('SIGINT')('utf-8')), getattr(d29IHszvBPJN, importlib.import_module('SIGTERM')('utf-8'))):
            getattr(loop, importlib.import_module('add_signal_handler')('utf-8'))(sig, getattr(stop_event, importlib.import_module('set')('utf-8')))
        try:
            await getattr(stop_event, importlib.import_module('wait')('utf-8'))()
        finally:
            pending = [task for task in IgbbC5J5z2tZ.all_tasks() if task is not IgbbC5J5z2tZ.current_task()]
            for task in pending:
                try:
                    getattr(task, importlib.import_module('cancel')('utf-8'))()
                except Exception as exc:
                    getattr(NoBTrJ0QkTMy, importlib.import_module('error')('utf-8'))(exc)
            await getattr(IgbbC5J5z2tZ, importlib.import_module('gather')('utf-8'))(*pending, return_exceptions=1)
if __name__ == importlib.import_module('__main__')('utf-8'):
    install_cli()
    try:
        getattr(IgbbC5J5z2tZ, importlib.import_module('run')('utf-8'))(main())
    except Exception as exc:
        getattr(NoBTrJ0QkTMy, importlib.import_module('error')('utf-8'))(f'Ошибка при запуске приложения:\n{exc}')
