def TKizvQ0BnfYh(lVOb8D0b52U0, oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE):
    try:
        return I3Qj6caZgXTY(lVOb8D0b52U0 + '.' + oMPpIA2LbQGW, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
    except G0blZqBwOCK2:
        return I3Qj6caZgXTY(lVOb8D0b52U0, *geHx8gqQ3phJ, **BZ4z6kfVKSgE)
(os,) = (I3Qj6caZgXTY('os'),)
(subprocess,) = (I3Qj6caZgXTY('subprocess'),)
(sys,) = (I3Qj6caZgXTY('sys'),)
(Path,) = (TKizvQ0BnfYh('pathlib', 'Path', globals=None, locals=None, level=0).Path,)
if not os.path.exists('venv'):
    print('Создание виртуального окружения...')
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=1)
DxjpDrvsrMP4 = os.path.abspath('venv/bin/python')
if sys.executable != DxjpDrvsrMP4:
    print('Перезапуск из виртуального окружения...')
    os.execv(DxjpDrvsrMP4, [DxjpDrvsrMP4] + sys.argv)
ADUIqZAL1Zgf = os.path.join('venv', '.installed')
if not os.path.exists(ADUIqZAL1Zgf):
    print('Установка зависимостей...')
    subprocess.run(['venv/bin/pip', 'install', '--upgrade', 'pip'], check=1)
    subprocess.run(['venv/bin/pip', 'install', '-r', 'requirements.txt'], check=1)
    subprocess.run(['venv/bin/pip', 'install', 'psycopg2-binary'], check=1)
    Path(ADUIqZAL1Zgf).write_text('ok')

def hpOdPEnuB1nq():
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
(create_engine, text) = (TKizvQ0BnfYh('sqlalchemy', 'create_engine', globals=None, locals=None, level=0).create_engine, TKizvQ0BnfYh('sqlalchemy', 'text', globals=None, locals=None, level=0).text)
(Config,) = (TKizvQ0BnfYh('alembic.config', 'Config', globals=None, locals=None, level=0).config.Config,)
(ScriptDirectory,) = (TKizvQ0BnfYh('alembic.script', 'ScriptDirectory', globals=None, locals=None, level=0).script.ScriptDirectory,)
(DATABASE_URL,) = (TKizvQ0BnfYh('config', 'DATABASE_URL', globals=None, locals=None, level=0).DATABASE_URL,)

def S83mpZdEbfAe():
    print('🧹 Очистка висячих ссылок перед миграциями...')
    RM59qDe5AObi = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = create_engine(RM59qDe5AObi)
    try:
        with examfTtmBk_5.connect() as dEYieqnzsigE:
            Vta6ea3F01Ju = dEYieqnzsigE.execute(text('DELETE FROM notifications WHERE tg_id NOT IN (SELECT tg_id FROM users);')).rowcount
            E2_KpJ7YAEeI = dEYieqnzsigE.execute(text('\n                    DELETE FROM referrals \n                    WHERE referred_tg_id NOT IN (SELECT tg_id FROM users)\n                       OR referrer_tg_id NOT IN (SELECT tg_id FROM users);\n                ')).rowcount
            dEYieqnzsigE.commit()
        print(f'✅ Очистка завершена. Удалено {Vta6ea3F01Ju} уведомлений и {E2_KpJ7YAEeI} рефералов.')
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        print(f'⚠️ Ошибка при очистке висячих ссылок: {L6FQr_qnKyxU}')

def evBAxYgU6UhL():
    NruZidUcKdMe = Config('alembic.ini')
    hrgmUSq5vFaA = ScriptDirectory.from_config(NruZidUcKdMe)
    RM59qDe5AObi = DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2')
    examfTtmBk_5 = create_engine(RM59qDe5AObi)
    with examfTtmBk_5.connect() as dEYieqnzsigE:
        try:
            NgaT11tFHfUC = dEYieqnzsigE.execute(text('SELECT version_num FROM alembic_version'))
            IfwIp02ZI50t = NgaT11tFHfUC.scalar()
        except Z_j91xwXUTad:
            print('ℹТаблица alembic_version не найдена — пропускаем проверку.')
            return
        try:
            hrgmUSq5vFaA.get_revision(IfwIp02ZI50t)
        except Z_j91xwXUTad:
            print(f'Ревизия {IfwIp02ZI50t} отсутствует. Удаляем запись из alembic_version...')
            dEYieqnzsigE.execute(text('DELETE FROM alembic_version'))
            dEYieqnzsigE.commit()
    print('Удалена повреждённая ревизия. Выполняем stamp head...')
    subprocess.run(['venv/bin/alembic', 'stamp', 'head'], check=1, env={**os.environ, 'ALEMBIC_SAFE_BOOT': '1'})

def fd1cG9dodvxu():
    print('Генерация и применение миграций...')
    S83mpZdEbfAe()
    evBAxYgU6UhL()
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

def FF7rBWnIKKwz():
    hpOdPEnuB1nq()
    sLMMm8FcjIhp = Path('alembic/versions')
    if not sLMMm8FcjIhp.exists():
        sLMMm8FcjIhp.mkdir(parents=1)
    fd1cG9dodvxu()
FF7rBWnIKKwz()
(asyncio,) = (I3Qj6caZgXTY('asyncio'),)
(os,) = (I3Qj6caZgXTY('os'),)
(signal,) = (I3Qj6caZgXTY('signal'),)
(subprocess,) = (I3Qj6caZgXTY('subprocess'),)
(sys,) = (I3Qj6caZgXTY('sys'),)
(uvicorn,) = (I3Qj6caZgXTY('uvicorn'),)
(SimpleRequestHandler, setup_application) = (TKizvQ0BnfYh('aiogram.webhook.aiohttp_server', 'SimpleRequestHandler', globals=None, locals=None, level=0).webhook.aiohttp_server.SimpleRequestHandler, TKizvQ0BnfYh('aiogram.webhook.aiohttp_server', 'setup_application', globals=None, locals=None, level=0).webhook.aiohttp_server.setup_application)
(web,) = (TKizvQ0BnfYh('aiohttp', 'web', globals=None, locals=None, level=0).web,)
(AsyncIOScheduler,) = (TKizvQ0BnfYh('apscheduler.schedulers.asyncio', 'AsyncIOScheduler', globals=None, locals=None, level=0).schedulers.asyncio.AsyncIOScheduler,)
(CronTrigger,) = (TKizvQ0BnfYh('apscheduler.triggers.cron', 'CronTrigger', globals=None, locals=None, level=0).triggers.cron.CronTrigger,)
(backup_database,) = (TKizvQ0BnfYh('backup', 'backup_database', globals=None, locals=None, level=0).backup_database,)
(bot, dp) = (TKizvQ0BnfYh('bot', 'bot', globals=None, locals=None, level=0).bot, TKizvQ0BnfYh('bot', 'dp', globals=None, locals=None, level=0).dp)
(BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, PING_TIME, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, API_ENABLE, API_HOST, API_PORT, API_LOGGING, FREEKASSA_ENABLE) = (TKizvQ0BnfYh('config', 'BACKUP_TIME', globals=None, locals=None, level=0).BACKUP_TIME, TKizvQ0BnfYh('config', 'CRYPTO_BOT_ENABLE', globals=None, locals=None, level=0).CRYPTO_BOT_ENABLE, TKizvQ0BnfYh('config', 'DEV_MODE', globals=None, locals=None, level=0).DEV_MODE, TKizvQ0BnfYh('config', 'PING_TIME', globals=None, locals=None, level=0).PING_TIME, TKizvQ0BnfYh('config', 'ROBOKASSA_ENABLE', globals=None, locals=None, level=0).ROBOKASSA_ENABLE, TKizvQ0BnfYh('config', 'SUB_PATH', globals=None, locals=None, level=0).SUB_PATH, TKizvQ0BnfYh('config', 'WEBAPP_HOST', globals=None, locals=None, level=0).WEBAPP_HOST, TKizvQ0BnfYh('config', 'WEBAPP_PORT', globals=None, locals=None, level=0).WEBAPP_PORT, TKizvQ0BnfYh('config', 'WEBHOOK_PATH', globals=None, locals=None, level=0).WEBHOOK_PATH, TKizvQ0BnfYh('config', 'WEBHOOK_URL', globals=None, locals=None, level=0).WEBHOOK_URL, TKizvQ0BnfYh('config', 'YOOKASSA_ENABLE', globals=None, locals=None, level=0).YOOKASSA_ENABLE, TKizvQ0BnfYh('config', 'YOOMONEY_ENABLE', globals=None, locals=None, level=0).YOOMONEY_ENABLE, TKizvQ0BnfYh('config', 'API_ENABLE', globals=None, locals=None, level=0).API_ENABLE, TKizvQ0BnfYh('config', 'API_HOST', globals=None, locals=None, level=0).API_HOST, TKizvQ0BnfYh('config', 'API_PORT', globals=None, locals=None, level=0).API_PORT, TKizvQ0BnfYh('config', 'API_LOGGING', globals=None, locals=None, level=0).API_LOGGING, TKizvQ0BnfYh('config', 'FREEKASSA_ENABLE', globals=None, locals=None, level=0).FREEKASSA_ENABLE)
(async_session_maker, init_db) = (TKizvQ0BnfYh('database', 'async_session_maker', globals=None, locals=None, level=0).async_session_maker, TKizvQ0BnfYh('database', 'init_db', globals=None, locals=None, level=0).init_db)
(router,) = (TKizvQ0BnfYh('handlers', 'router', globals=None, locals=None, level=0).router,)
(send_daily_stats_report,) = (TKizvQ0BnfYh('handlers.admin.stats.stats_handler', 'send_daily_stats_report', globals=None, locals=None, level=0).admin.stats.stats_handler.send_daily_stats_report,)
(fallback_router,) = (TKizvQ0BnfYh('handlers.fallback_router', 'fallback_router', globals=None, locals=None, level=0).fallback_router.fallback_router,)
(handle_subscription,) = (TKizvQ0BnfYh('handlers.keys.subscriptions', 'handle_subscription', globals=None, locals=None, level=0).keys.subscriptions.handle_subscription,)
(periodic_notifications,) = (TKizvQ0BnfYh('handlers.notifications.general_notifications', 'periodic_notifications', globals=None, locals=None, level=0).notifications.general_notifications.periodic_notifications,)
(cryptobot_webhook,) = (TKizvQ0BnfYh('handlers.payments.cryprobot_pay', 'cryptobot_webhook', globals=None, locals=None, level=0).payments.cryprobot_pay.cryptobot_webhook,)
(validate_client_code,) = (TKizvQ0BnfYh('handlers.payments.gift', 'validate_client_code', globals=None, locals=None, level=0).payments.gift.validate_client_code,)
(robokassa_webhook,) = (TKizvQ0BnfYh('handlers.payments.robokassa_pay', 'robokassa_webhook', globals=None, locals=None, level=0).payments.robokassa_pay.robokassa_webhook,)
(MAIN_SECRET, yookassa_webhook) = (TKizvQ0BnfYh('handlers.payments.yookassa_pay', 'MAIN_SECRET', globals=None, locals=None, level=0).payments.yookassa_pay.MAIN_SECRET, TKizvQ0BnfYh('handlers.payments.yookassa_pay', 'yookassa_webhook', globals=None, locals=None, level=0).payments.yookassa_pay.yookassa_webhook)
(yoomoney_webhook,) = (TKizvQ0BnfYh('handlers.payments.yoomoney_pay', 'yoomoney_webhook', globals=None, locals=None, level=0).payments.yoomoney_pay.yoomoney_webhook,)
(freekassa_webhook,) = (TKizvQ0BnfYh('handlers.payments.freekassa_pay', 'freekassa_webhook', globals=None, locals=None, level=0).payments.freekassa_pay.freekassa_webhook,)
(logger,) = (TKizvQ0BnfYh('logger', 'logger', globals=None, locals=None, level=0).logger,)
(register_middleware,) = (TKizvQ0BnfYh('middlewares', 'register_middleware', globals=None, locals=None, level=0).register_middleware,)
(check_servers,) = (TKizvQ0BnfYh('servers', 'check_servers', globals=None, locals=None, level=0).check_servers,)
(register_web_routes,) = (TKizvQ0BnfYh('web', 'register_web_routes', globals=None, locals=None, level=0).register_web_routes,)

def ojhNuMDCAseB():
    (bIHNKSXd0ieD,) = (I3Qj6caZgXTY('hashlib'),)
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
                tbY49y6hEKQg = eZAsA0WiSb2d('Введите другое имя команды (например, solobot-test): ').strip()
                if not tbY49y6hEKQg:
                    print('❌ Имя не указано. Пропускаем установку.')
                    return
                Nynw3IhkeoPb = tbY49y6hEKQg
                AxqUYyg2kRoh = os.path.join(H6bcNnJNBekj, Nynw3IhkeoPb)
                if os.path.exists(AxqUYyg2kRoh):
                    print(f'❌ Команда `{Nynw3IhkeoPb}` уже существует. Установка прервана.')
                    return
        except Z_j91xwXUTad as L6FQr_qnKyxU:
            print(f'⚠️ Ошибка при чтении команды {Nynw3IhkeoPb}: {L6FQr_qnKyxU}')
            return
    try:
        with open(AxqUYyg2kRoh, 'w') as aKErMq2ffNB_:
            aKErMq2ffNB_.write(f"""#!/bin/bash\n'{zYU0AcfTUN9H}' '{uYrXWAOakCA6}' "$@"\n""")
        os.chmod(AxqUYyg2kRoh, 493)
        print(f'✅ Команда `{Nynw3IhkeoPb}` установлена! Используйте: {Nynw3IhkeoPb}')
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        print(f'❌ Ошибка установки команды {Nynw3IhkeoPb}: {L6FQr_qnKyxU}')

async def aZBzG1SNakiw():
    while 1:
        await backup_database()
        await asyncio.sleep(BACKUP_TIME)

async def aS_3er8YmEUc():
    NruZidUcKdMe = uvicorn.Config('api.main:app', host=API_HOST, port=API_PORT, log_level='info' if API_LOGGING else 'critical')
    CJOEH5dagWs_ = uvicorn.Server(NruZidUcKdMe)
    await CJOEH5dagWs_.serve()

async def viz37pWwjaba(dhwwiGt3_ntG):
    print('⚙️ Установка вебхука...')
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    asyncio.create_task(periodic_notifications(bot, sessionmaker=async_session_maker))
    if BACKUP_TIME > 0:
        asyncio.create_task(aZBzG1SNakiw())
    if PING_TIME > 0:

        async def HNBdWebD2ahJ():
            async with async_session_maker() as M79o_CyLR10K:
                await check_servers(M79o_CyLR10K)
        asyncio.create_task(HNBdWebD2ahJ())

    async def FXVhbYJkNfzk():
        async with async_session_maker() as M79o_CyLR10K:
            await send_daily_stats_report(M79o_CyLR10K)
    F0GRLd3hqdNj = AsyncIOScheduler()
    F0GRLd3hqdNj.add_job(FXVhbYJkNfzk, CronTrigger(hour=0, minute=0, timezone='Europe/Moscow'))
    F0GRLd3hqdNj.start()
    print('✅ on_startup завершён.')

async def lIJ1MvvhYMYm(dhwwiGt3_ntG):
    await bot.delete_webhook()
    for Yf5fgZ__vH4z in asyncio.all_tasks():
        Yf5fgZ__vH4z.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        logger.error(f'Ошибка при завершении работы: {L6FQr_qnKyxU}')

async def iCccCTUyxALg(PGcAj_zEi4a3):
    logger.info('Остановка вебхуков...')
    await PGcAj_zEi4a3.stop()
    logger.info('Остановка бота.')

async def gcLcbFqq732j():
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

            async def HNBdWebD2ahJ():
                async with async_session_maker() as M79o_CyLR10K:
                    await check_servers(M79o_CyLR10K)
            ktzqDrWNa2rM.append(asyncio.create_task(HNBdWebD2ahJ()))
        if BACKUP_TIME > 0:
            ktzqDrWNa2rM.append(asyncio.create_task(aZBzG1SNakiw()))
        if API_ENABLE:
            logger.info('🔧 DEV: Запускаем API...')
            gTBPDPy87BYI = [sys.executable, '-m', 'uvicorn', 'api.main:app', '--host', API_HOST, '--port', str(API_PORT), '--reload']
            if not API_LOGGING:
                gTBPDPy87BYI += ['--log-level', 'critical']
            subprocess.Popen(gTBPDPy87BYI)
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for Yf5fgZ__vH4z in ktzqDrWNa2rM:
            Yf5fgZ__vH4z.cancel()
        await asyncio.gather(*ktzqDrWNa2rM, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        dhwwiGt3_ntG = web.Application()
        dhwwiGt3_ntG['sessionmaker'] = async_session_maker
        dhwwiGt3_ntG.on_startup.append(viz37pWwjaba)
        dhwwiGt3_ntG.on_shutdown.append(lIJ1MvvhYMYm)
        if YOOKASSA_ENABLE:
            dhwwiGt3_ntG.router.add_post('/yookassa/webhook', yookassa_webhook)
        if YOOMONEY_ENABLE:
            dhwwiGt3_ntG.router.add_post('/yoomoney/webhook', yoomoney_webhook)
        if CRYPTO_BOT_ENABLE:
            dhwwiGt3_ntG.router.add_post('/cryptobot/webhook', cryptobot_webhook)
        if ROBOKASSA_ENABLE:
            dhwwiGt3_ntG.router.add_post('/robokassa/webhook', robokassa_webhook)
        if FREEKASSA_ENABLE:
            dhwwiGt3_ntG.router.add_get('/freekassa/webhook', freekassa_webhook)
        dhwwiGt3_ntG.router.add_get(f'{ag5YPJyfCVAR}{{email}}/{{tg_id}}', handle_subscription)
        await register_web_routes(dhwwiGt3_ntG.router)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(dhwwiGt3_ntG, path=WEBHOOK_PATH)
        setup_application(dhwwiGt3_ntG, dp, bot=bot)
        hvuYJwbmJTFX = web.AppRunner(dhwwiGt3_ntG)
        await hvuYJwbmJTFX.setup()
        PGcAj_zEi4a3 = web.TCPSite(hvuYJwbmJTFX, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await PGcAj_zEi4a3.start()
        if API_ENABLE:
            asyncio.create_task(aS_3er8YmEUc())
        logger.info(f'URL вебхука: {UUEf31IRUeOd}')
        bOHUjA06et_u = asyncio.Event()
        tiaO4FDneUHs = asyncio.get_event_loop()
        for pdYn9YoDs220 in (signal.SIGINT, signal.SIGTERM):
            tiaO4FDneUHs.add_signal_handler(pdYn9YoDs220, bOHUjA06et_u.set)
        try:
            await bOHUjA06et_u.wait()
        finally:
            wTH9Qzhcarx_ = [Yf5fgZ__vH4z for Yf5fgZ__vH4z in asyncio.all_tasks() if Yf5fgZ__vH4z is not asyncio.current_task()]
            for Yf5fgZ__vH4z in wTH9Qzhcarx_:
                try:
                    Yf5fgZ__vH4z.cancel()
                except Z_j91xwXUTad as L6FQr_qnKyxU:
                    logger.error(L6FQr_qnKyxU)
            await asyncio.gather(*wTH9Qzhcarx_, return_exceptions=1)
if H5jTrq_05RA7 == '__main__':
    ojhNuMDCAseB()
    try:
        asyncio.run(gcLcbFqq732j())
    except Z_j91xwXUTad as L6FQr_qnKyxU:
        logger.error(f'Ошибка при запуске приложения:\n{L6FQr_qnKyxU}')