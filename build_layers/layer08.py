def TKizvQ0BnfYh(lVOb8D0b52U0, oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE):
    try:
        return __import__(lVOb8D0b52U0 + '.' + oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
    except G0blZqBwOCK2:
        return __import__(lVOb8D0b52U0, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
FyYEeTFyaEwm, = (__import__('os'),)
UhKVW6ci2ufp, = (__import__('subprocess'),)
NlMf_Ll9d9TE, = (__import__('sys'),)
iZQnRId6lk4a, = (TKizvQ0BnfYh('pathlib', 'Path', globals=None, locals=None, level=0).Path,)
if not FyYEeTFyaEwm.path.exists('venv'):
    print('Создание виртуального окружения...')
    UhKVW6ci2ufp.run([NlMf_Ll9d9TE.executable, '-m', 'venv', 'venv'], check=1)
DxjpDrvsrMP4 = FyYEeTFyaEwm.path.abspath('venv/bin/python')
if NlMf_Ll9d9TE.executable != DxjpDrvsrMP4:
    print('Перезапуск из виртуального окружения...')
    FyYEeTFyaEwm.execv(DxjpDrvsrMP4, [DxjpDrvsrMP4] + NlMf_Ll9d9TE.argv)
ADUIqZAL1Zgf = FyYEeTFyaEwm.path.join('venv', '.installed')
if not FyYEeTFyaEwm.path.exists(ADUIqZAL1Zgf):
    print('Установка зависимостей...')
    UhKVW6ci2ufp.run(['venv/bin/pip', 'install', '--upgrade', 'pip'], check=1)
    UhKVW6ci2ufp.run(['venv/bin/pip', 'install', '-r', 'requirements.txt'], check=1)
    UhKVW6ci2ufp.run(['venv/bin/pip', 'install', 'psycopg2-binary'], check=1)
    iZQnRId6lk4a(ADUIqZAL1Zgf).write_text('ok')

def hpOdPEnuB1nq():
    A2OFynpSEGYZ = iZQnRId6lk4a('alembic/env.py')
    if A2OFynpSEGYZ.exists():
        print('ℹAlembic уже инициализирован.')
        return
    print('🛠️ Инициализация Alembic...')
    UhKVW6ci2ufp.run(['venv/bin/alembic', 'init', 'alembic'], check=1)
    if A2OFynpSEGYZ.exists():
        CRcKJ5Z0I1XF = A2OFynpSEGYZ.read_text()
        MHZivVbLpj_1 = 'from database.models import Base\nfrom config import DATABASE_URL\n# Заменяем asyncpg на psycopg2 только для миграций\nsync_url = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")\nconfig.set_main_option("sqlalchemy.url", sync_url)\n\ntarget_metadata = Base.metadata'
        CRcKJ5Z0I1XF = CRcKJ5Z0I1XF.replace('target_metadata = None', MHZivVbLpj_1)
        A2OFynpSEGYZ.write_text(CRcKJ5Z0I1XF)
    print('✅ Alembic инициализирован.')
Q7tClP07Cr24, CRcKJ5Z0I1XF = (TKizvQ0BnfYh('sqlalchemy', 'create_engine', globals=None, locals=None, level=0).create_engine, TKizvQ0BnfYh('sqlalchemy', 'text', globals=None, locals=None, level=0).text)
kYsphmT4sjV8, = (TKizvQ0BnfYh('alembic.config', 'Config', globals=None, locals=None, level=0).config.Config,)
bX0dgRLufyU9, = (TKizvQ0BnfYh('alembic.script', 'ScriptDirectory', globals=None, locals=None, level=0).script.ScriptDirectory,)
etiivloU5GNO, = (TKizvQ0BnfYh('config', 'DATABASE_URL', globals=None, locals=None, level=0).DATABASE_URL,)

def S83mpZdEbfAe():
    print('🧹 Очистка висячих ссылок перед миграциями...')
    RM59qDe5AObi = etiivloU5GNO.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = Q7tClP07Cr24(RM59qDe5AObi)
    try:
        with examfTtmBk_5.connect() as dEYieqnzsigE:
            Vta6ea3F01Ju = dEYieqnzsigE.execute(CRcKJ5Z0I1XF('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            E2_KpJ7YAEeI = dEYieqnzsigE.execute(CRcKJ5Z0I1XF('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            dEYieqnzsigE.commit()
        print(f'✅ Очистка завершена. Удалено {Vta6ea3F01Ju} уведомлений и {E2_KpJ7YAEeI} рефералов.')
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        print(f'⚠️ Ошибка при очистке висячих ссылок: {L6FQr_qnKyxU}')

def evBAxYgU6UhL():
    NruZidUcKdMe = kYsphmT4sjV8('alembic.ini')
    hrgmUSq5vFaA = bX0dgRLufyU9.from_config(NruZidUcKdMe)
    RM59qDe5AObi = etiivloU5GNO.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = Q7tClP07Cr24(RM59qDe5AObi)
    with examfTtmBk_5.connect() as dEYieqnzsigE:
        try:
            NgaT11tFHfUC = dEYieqnzsigE.execute(CRcKJ5Z0I1XF('SELECT version_num FROM alembic_version'))
            IfwIp02ZI50t = NgaT11tFHfUC.scalar()
        except Z_j91xwXUTad:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            hrgmUSq5vFaA.get_revision(IfwIp02ZI50t)
        except Z_j91xwXUTad:
            print(f'Ревизия {IfwIp02ZI50t} отсутствует. Удаляем запись из alembic_version...')
            dEYieqnzsigE.execute(CRcKJ5Z0I1XF('DELETE FROM alembic_version'))
            dEYieqnzsigE.commit()
    print('Удалена повреждённая ревизия. Выполняем stamp head...')
    UhKVW6ci2ufp.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**FyYEeTFyaEwm.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def fd1cG9dodvxu():
    print('Генерация и применение миграций...')
    S83mpZdEbfAe()
    evBAxYgU6UhL()
    NgaT11tFHfUC = UhKVW6ci2ufp.run(['venv/bin/alembic', 'revision', '--autogenerate', '-m', 'Auto migration'], capture_output=1, text=1)
    if 'No changes in schema detected' in NgaT11tFHfUC.stdout:
        print('ℹИзменений в моделях нет — миграция не требуется.')
    else:
        print('Миграция создана. Применяем...')
        Hvn5kk0_vFwt = UhKVW6ci2ufp.run(['venv/bin/alembic', 'upgrade', 'head'], capture_output=1, text=1)
        if Hvn5kk0_vFwt.returncode != 0:
            print('❌ Ошибка при применении миграции:')
            print('STDOUT:')
            print(Hvn5kk0_vFwt.stdout)
            print('STDERR:')
            print(Hvn5kk0_vFwt.stderr)
            NlMf_Ll9d9TE.exit(1)
        print('✅ Alembic upgrade успешно выполнен.')

def FF7rBWnIKKwz():
    hpOdPEnuB1nq()
    sLMMm8FcjIhp = iZQnRId6lk4a('alembic/versions')
    if not sLMMm8FcjIhp.exists():
        sLMMm8FcjIhp.mkdir(parents=1)
    fd1cG9dodvxu()
FF7rBWnIKKwz()
IgbbC5J5z2tZ, = (__import__('asyncio'),)
FyYEeTFyaEwm, = (__import__('os'),)
d29IHszvBPJN, = (__import__('signal'),)
UhKVW6ci2ufp, = (__import__('subprocess'),)
NlMf_Ll9d9TE, = (__import__('sys'),)
c5NNV3V3Ry3y, = (__import__('uvicorn'),)
dJnsTNALuDBU, dck_6UV5RWy6 = (TKizvQ0BnfYh('aiogram.webhook.aiohttp_server', 'SimpleRequestHandler', globals=None, locals=None, level=0).webhook.aiohttp_server.SimpleRequestHandler, TKizvQ0BnfYh('aiogram.webhook.aiohttp_server', 'setup_application', globals=None, locals=None, level=0).webhook.aiohttp_server.setup_application)
S16nYXJrI_8a, = (TKizvQ0BnfYh('aiohttp', 'web', globals=None, locals=None, level=0).web,)
dmkLf2NsdNqg, = (TKizvQ0BnfYh('apscheduler.schedulers.asyncio', 'AsyncIOScheduler', globals=None, locals=None, level=0).schedulers.asyncio.AsyncIOScheduler,)
CtAaFtUYmGm7, = (TKizvQ0BnfYh('apscheduler.triggers.cron', 'CronTrigger', globals=None, locals=None, level=0).triggers.cron.CronTrigger,)
LY5TOgVHXSy5, = (TKizvQ0BnfYh('backup', 'backup_database', globals=None, locals=None, level=0).backup_database,)
B1br9W7_bn2X, QawnGHulCbas = (TKizvQ0BnfYh('bot', 'bot', globals=None, locals=None, level=0).bot, TKizvQ0BnfYh('bot', 'dp', globals=None, locals=None, level=0).dp)
cOhAqchD95fm, gXLBwYTBCUt7, QH1oQYKrN7qd, DikaXCEDxTz2, hMtGAoAJKuQm, ag5YPJyfCVAR, iA9Ziao7fn9P, CU6sEfk1r5mF, n7zYTnBpvjmO, UUEf31IRUeOd, yP2r9gf4oG8a, xHfEv2FKkJDn, Nuk8G57TsVme, YKUElrdccEwu, vIr_pqkFXy3z, K9_RuISjrOaT, Q51yqS3LP9Ft = (TKizvQ0BnfYh('config', 'BACKUP_TIME', globals=None, locals=None, level=0).BACKUP_TIME, TKizvQ0BnfYh('config', 'CRYPTO_BOT_ENABLE', globals=None, locals=None, level=0).CRYPTO_BOT_ENABLE, TKizvQ0BnfYh('config', 'DEV_MODE', globals=None, locals=None, level=0).DEV_MODE, TKizvQ0BnfYh('config', 'PING_TIME', globals=None, locals=None, level=0).PING_TIME, TKizvQ0BnfYh('config', 'ROBOKASSA_ENABLE', globals=None, locals=None, level=0).ROBOKASSA_ENABLE, TKizvQ0BnfYh('config', 'SUB_PATH', globals=None, locals=None, level=0).SUB_PATH, TKizvQ0BnfYh('config', 'WEBAPP_HOST', globals=None, locals=None, level=0).WEBAPP_HOST, TKizvQ0BnfYh('config', 'WEBAPP_PORT', globals=None, locals=None, level=0).WEBAPP_PORT, TKizvQ0BnfYh('config', 'WEBHOOK_PATH', globals=None, locals=None, level=0).WEBHOOK_PATH, TKizvQ0BnfYh('config', 'WEBHOOK_URL', globals=None, locals=None, level=0).WEBHOOK_URL, TKizvQ0BnfYh('config', 'YOOKASSA_ENABLE', globals=None, locals=None, level=0).YOOKASSA_ENABLE, TKizvQ0BnfYh('config', 'YOOMONEY_ENABLE', globals=None, locals=None, level=0).YOOMONEY_ENABLE, TKizvQ0BnfYh('config', 'API_ENABLE', globals=None, locals=None, level=0).API_ENABLE, TKizvQ0BnfYh('config', 'API_HOST', globals=None, locals=None, level=0).API_HOST, TKizvQ0BnfYh('config', 'API_PORT', globals=None, locals=None, level=0).API_PORT, TKizvQ0BnfYh('config', 'API_LOGGING', globals=None, locals=None, level=0).API_LOGGING, TKizvQ0BnfYh('config', 'FREEKASSA_ENABLE', globals=None, locals=None, level=0).FREEKASSA_ENABLE)
cUt_1v7BqmdG, Q0676_Ys6MDk = (TKizvQ0BnfYh('database', 'async_session_maker', globals=None, locals=None, level=0).async_session_maker, TKizvQ0BnfYh('database', 'init_db', globals=None, locals=None, level=0).init_db)
Nnx4UIsVD5DW, = (TKizvQ0BnfYh('handlers', 'router', globals=None, locals=None, level=0).router,)
Nl3wzY0MRxUb, = (TKizvQ0BnfYh('handlers.admin.stats.stats_handler', 'send_daily_stats_report', globals=None, locals=None, level=0).admin.stats.stats_handler.send_daily_stats_report,)
Lj61wtQvyyYG, = (TKizvQ0BnfYh('handlers.fallback_router', 'fallback_router', globals=None, locals=None, level=0).fallback_router.fallback_router,)
_QMVLJZw6AAl, = (TKizvQ0BnfYh('handlers.keys.subscriptions', 'handle_subscription', globals=None, locals=None, level=0).keys.subscriptions.handle_subscription,)
w0n_fSKiXLno, = (TKizvQ0BnfYh('handlers.notifications.general_notifications', 'periodic_notifications', globals=None, locals=None, level=0).notifications.general_notifications.periodic_notifications,)
BI8caSrsEQLn, = (TKizvQ0BnfYh('handlers.payments.cryprobot_pay', 'cryptobot_webhook', globals=None, locals=None, level=0).payments.cryprobot_pay.cryptobot_webhook,)
fTh9BL4qlePy, = (TKizvQ0BnfYh('handlers.payments.gift', 'validate_client_code', globals=None, locals=None, level=0).payments.gift.validate_client_code,)
YIDxn0At0JLm, = (TKizvQ0BnfYh('handlers.payments.robokassa_pay', 'robokassa_webhook', globals=None, locals=None, level=0).payments.robokassa_pay.robokassa_webhook,)
zHROqa7Vv7S4, yQcDOUG0lwO3 = (TKizvQ0BnfYh('handlers.payments.yookassa_pay', 'MAIN_SECRET', globals=None, locals=None, level=0).payments.yookassa_pay.MAIN_SECRET, TKizvQ0BnfYh('handlers.payments.yookassa_pay', 'yookassa_webhook', globals=None, locals=None, level=0).payments.yookassa_pay.yookassa_webhook)
CysYC_WVi6QN, = (TKizvQ0BnfYh('handlers.payments.yoomoney_pay', 'yoomoney_webhook', globals=None, locals=None, level=0).payments.yoomoney_pay.yoomoney_webhook,)
CWTIC90Zi1Jk, = (TKizvQ0BnfYh('handlers.payments.freekassa_pay', 'freekassa_webhook', globals=None, locals=None, level=0).payments.freekassa_pay.freekassa_webhook,)
NoBTrJ0QkTMy, = (TKizvQ0BnfYh('logger', 'logger', globals=None, locals=None, level=0).logger,)
lrMgLENzItNN, = (TKizvQ0BnfYh('middlewares', 'register_middleware', globals=None, locals=None, level=0).register_middleware,)
KI__IpMinSme, = (TKizvQ0BnfYh('servers', 'check_servers', globals=None, locals=None, level=0).check_servers,)
vuUwn1WIpDH1, = (TKizvQ0BnfYh('web', 'register_web_routes', globals=None, locals=None, level=0).register_web_routes,)

def ojhNuMDCAseB():
    bIHNKSXd0ieD, = (__import__('hashlib'),)
    uYrXWAOakCA6 = FyYEeTFyaEwm.path.abspath('cli_launcher.py')
    zYU0AcfTUN9H = NlMf_Ll9d9TE.executable
    N5BOS5Ba7iBe = ['/usr/local/bin', '/usr/bin', FyYEeTFyaEwm.path.expanduser('~/.local/bin')]
    for H6bcNnJNBekj in N5BOS5Ba7iBe:
        if FyYEeTFyaEwm.path.isdir(H6bcNnJNBekj) and FyYEeTFyaEwm.access(H6bcNnJNBekj, FyYEeTFyaEwm.W_OK):
            break
    else:
        print('❌ Не удалось найти подходящий каталог для установки команды.')
        return
    pEfQPe06_bNU = 'solobot'
    Nynw3IhkeoPb = pEfQPe06_bNU
    AxqUYyg2kRoh = FyYEeTFyaEwm.path.join(H6bcNnJNBekj, Nynw3IhkeoPb)
    if FyYEeTFyaEwm.path.exists(AxqUYyg2kRoh):
        try:
            with open(AxqUYyg2kRoh, 'r') as aKErMq2ffNB_:
                t09X61UaTZUU = aKErMq2ffNB_.read()
            if uYrXWAOakCA6 in t09X61UaTZUU:
                return
            else:
                print(f'⚠️ Команда `{Nynw3IhkeoPb}` уже установлена, но для другой копии бота.')
                tbY49y6hEKQg = eZAsA0WiSb2d('Введите другое имя команды (например, solobot-test): ').strip()
                if not tbY49y6hEKQg:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                Nynw3IhkeoPb = tbY49y6hEKQg
                AxqUYyg2kRoh = FyYEeTFyaEwm.path.join(H6bcNnJNBekj, Nynw3IhkeoPb)
                if FyYEeTFyaEwm.path.exists(AxqUYyg2kRoh):
                    print(f'❌ Команда `{Nynw3IhkeoPb}` уже существует. Установка прервана.')
                    return
        except Z_j91xwXUTad as L6FQr_qnKyxU:
            print(f'⚠️ Ошибка при чтении команды {Nynw3IhkeoPb}: {L6FQr_qnKyxU}')
            return
    try:
        with open(AxqUYyg2kRoh, 'w') as aKErMq2ffNB_:
            aKErMq2ffNB_.write(f"""#!/bin/bash\n'{zYU0AcfTUN9H}' '{uYrXWAOakCA6}' "$@"\n""")
        FyYEeTFyaEwm.chmod(AxqUYyg2kRoh, 493)
        print(f'✅ Команда `{Nynw3IhkeoPb}` установлена! Используйте: {Nynw3IhkeoPb}')
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        print(f'❌ Ошибка установки команды {Nynw3IhkeoPb}: {L6FQr_qnKyxU}')

async def aZBzG1SNakiw():
    while 1:
        await LY5TOgVHXSy5()
        await IgbbC5J5z2tZ.sleep(cOhAqchD95fm)

async def aS_3er8YmEUc():
    NruZidUcKdMe = c5NNV3V3Ry3y.Config('api.main:app', host=YKUElrdccEwu, port=vIr_pqkFXy3z, log_level='info' if K9_RuISjrOaT else 'critical')
    CJOEH5dagWs_ = c5NNV3V3Ry3y.Server(NruZidUcKdMe)
    await CJOEH5dagWs_.serve()

async def viz37pWwjaba(dhwwiGt3_ntG):
    print('⚙️ Установка вебхука...')
    await B1br9W7_bn2X.set_webhook(UUEf31IRUeOd)
    await Q0676_Ys6MDk()
    IgbbC5J5z2tZ.create_task(w0n_fSKiXLno(B1br9W7_bn2X, sessionmaker=cUt_1v7BqmdG))
    if cOhAqchD95fm > 0:
        IgbbC5J5z2tZ.create_task(aZBzG1SNakiw())
    if DikaXCEDxTz2 > 0:

        async def HNBdWebD2ahJ():
            async with cUt_1v7BqmdG() as M79o_CyLR10K:
                await KI__IpMinSme(M79o_CyLR10K)
        IgbbC5J5z2tZ.create_task(HNBdWebD2ahJ())

    async def FXVhbYJkNfzk():
        async with cUt_1v7BqmdG() as M79o_CyLR10K:
            await Nl3wzY0MRxUb(M79o_CyLR10K)
    F0GRLd3hqdNj = dmkLf2NsdNqg()
    F0GRLd3hqdNj.add_job(FXVhbYJkNfzk, CtAaFtUYmGm7(hour=0, minute=0, timezone='Europe/Moscow'))
    F0GRLd3hqdNj.start()
    print('✅ on_startup завершён.')

async def lIJ1MvvhYMYm(dhwwiGt3_ntG):
    await B1br9W7_bn2X.delete_webhook()
    for Yf5fgZ__vH4z in IgbbC5J5z2tZ.all_tasks():
        Yf5fgZ__vH4z.cancel()
    try:
        await IgbbC5J5z2tZ.gather(*IgbbC5J5z2tZ.all_tasks(), return_exceptions=1)
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        NoBTrJ0QkTMy.error(f'Ошибка при завершении работы: {L6FQr_qnKyxU}')

async def iCccCTUyxALg(PGcAj_zEi4a3):
    NoBTrJ0QkTMy.info('Остановка вебхуков...')
    await PGcAj_zEi4a3.stop()
    NoBTrJ0QkTMy.info('Остановка бота.')

async def gcLcbFqq732j():
    bZnyVT5QtFH6 = await fTh9BL4qlePy()
    if not bZnyVT5QtFH6:
        print('❌ Бот не активирован. Проверьте ваш клиентский код.')
        NlMf_Ll9d9TE.exit(1)
    DAfvdd0x1Xo6 = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if zHROqa7Vv7S4 != DAfvdd0x1Xo6:
        NoBTrJ0QkTMy.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    lrMgLENzItNN(QawnGHulCbas, sessionmaker=cUt_1v7BqmdG)
    QawnGHulCbas.include_router(Nnx4UIsVD5DW)
    QawnGHulCbas.include_router(Lj61wtQvyyYG)
    if QH1oQYKrN7qd:
        NoBTrJ0QkTMy.info('Запуск в режиме разработки...')
        await B1br9W7_bn2X.delete_webhook()
        await Q0676_Ys6MDk()
        ktzqDrWNa2rM = [IgbbC5J5z2tZ.create_task(w0n_fSKiXLno(B1br9W7_bn2X, sessionmaker=cUt_1v7BqmdG))]
        if DikaXCEDxTz2 > 0:

            async def HNBdWebD2ahJ():
                async with cUt_1v7BqmdG() as M79o_CyLR10K:
                    await KI__IpMinSme(M79o_CyLR10K)
            ktzqDrWNa2rM.append(IgbbC5J5z2tZ.create_task(HNBdWebD2ahJ()))
        if cOhAqchD95fm > 0:
            ktzqDrWNa2rM.append(IgbbC5J5z2tZ.create_task(aZBzG1SNakiw()))
        if Nuk8G57TsVme:
            NoBTrJ0QkTMy.info('🔧 DEV: Запускаем API...')
            gTBPDPy87BYI = [NlMf_Ll9d9TE.executable, '-m', 'uvicorn', 'api.main:app', '--host', YKUElrdccEwu, '--port', str(vIr_pqkFXy3z), '--reload']
            if not K9_RuISjrOaT:
                gTBPDPy87BYI += ['--log-level', 'critical']
            UhKVW6ci2ufp.Popen(gTBPDPy87BYI)
        await QawnGHulCbas.start_polling(B1br9W7_bn2X)
        NoBTrJ0QkTMy.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for Yf5fgZ__vH4z in ktzqDrWNa2rM:
            Yf5fgZ__vH4z.cancel()
        await IgbbC5J5z2tZ.gather(*ktzqDrWNa2rM, return_exceptions=1)
    else:
        NoBTrJ0QkTMy.info('Запуск в production режиме...')
        dhwwiGt3_ntG = S16nYXJrI_8a.Application()
        dhwwiGt3_ntG['sessionmaker'] = cUt_1v7BqmdG
        dhwwiGt3_ntG.on_startup.append(viz37pWwjaba)
        dhwwiGt3_ntG.on_shutdown.append(lIJ1MvvhYMYm)
        if yP2r9gf4oG8a:
            dhwwiGt3_ntG.router.add_post('/yookassa/webhook', yQcDOUG0lwO3)
        if xHfEv2FKkJDn:
            dhwwiGt3_ntG.router.add_post('/yoomoney/webhook', CysYC_WVi6QN)
        if gXLBwYTBCUt7:
            dhwwiGt3_ntG.router.add_post('/cryptobot/webhook', BI8caSrsEQLn)
        if hMtGAoAJKuQm:
            dhwwiGt3_ntG.router.add_post('/robokassa/webhook', YIDxn0At0JLm)
        if Q51yqS3LP9Ft:
            dhwwiGt3_ntG.router.add_get('/freekassa/webhook', CWTIC90Zi1Jk)
        dhwwiGt3_ntG.router.add_get(f'{ag5YPJyfCVAR}{{email}}/{{tg_id}}', _QMVLJZw6AAl)
        await vuUwn1WIpDH1(dhwwiGt3_ntG.router)
        dJnsTNALuDBU(dispatcher=QawnGHulCbas, bot=B1br9W7_bn2X).register(dhwwiGt3_ntG, path=n7zYTnBpvjmO)
        dck_6UV5RWy6(dhwwiGt3_ntG, QawnGHulCbas, bot=B1br9W7_bn2X)
        hvuYJwbmJTFX = S16nYXJrI_8a.AppRunner(dhwwiGt3_ntG)
        await hvuYJwbmJTFX.setup()
        PGcAj_zEi4a3 = S16nYXJrI_8a.TCPSite(hvuYJwbmJTFX, host=iA9Ziao7fn9P, port=CU6sEfk1r5mF)
        await PGcAj_zEi4a3.start()
        if Nuk8G57TsVme:
            IgbbC5J5z2tZ.create_task(aS_3er8YmEUc())
        NoBTrJ0QkTMy.info(f'URL вебхука: {UUEf31IRUeOd}')
        bOHUjA06et_u = IgbbC5J5z2tZ.Event()
        tiaO4FDneUHs = IgbbC5J5z2tZ.get_event_loop()
        for pdYn9YoDs220 in (d29IHszvBPJN.SIGINT, d29IHszvBPJN.SIGTERM):
            tiaO4FDneUHs.add_signal_handler(pdYn9YoDs220, bOHUjA06et_u.set)
        try:
            await bOHUjA06et_u.wait()
        finally:
            wTH9Qzhcarx_ = [Yf5fgZ__vH4z for Yf5fgZ__vH4z in IgbbC5J5z2tZ.all_tasks() if Yf5fgZ__vH4z is not IgbbC5J5z2tZ.current_task()]
            for Yf5fgZ__vH4z in wTH9Qzhcarx_:
                try:
                    Yf5fgZ__vH4z.cancel()
                except Z_j91xwXUTad as L6FQr_qnKyxU:
                    NoBTrJ0QkTMy.error(L6FQr_qnKyxU)
            await IgbbC5J5z2tZ.gather(*wTH9Qzhcarx_, return_exceptions=1)
if H5jTrq_05RA7 == '__main__':
    ojhNuMDCAseB()
    try:
        IgbbC5J5z2tZ.run(gcLcbFqq732j())
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        NoBTrJ0QkTMy.error(f'Ошибка при запуске приложения:\n{L6FQr_qnKyxU}')