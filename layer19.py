import importlib
asyncio = (__import__('asyncio'),)
signal = (__import__('signal'),)
(SimpleRequestHandler, setup_application) = (importlib.import_module('aiogram.webhook.aiohttp_server').SimpleRequestHandler.webhook.aiohttp_server.SimpleRequestHandler, importlib.import_module('aiogram.webhook.aiohttp_server').setup_application.webhook.aiohttp_server.setup_application)
web = (importlib.import_module('aiohttp').web.web,)
backup_database = (importlib.import_module('backup').backup_database.backup_database,)
(bot, dp) = (importlib.import_module('bot').bot.bot, importlib.import_module('bot').dp.dp)
(BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, LEGACY_ENABLE, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, PING_TIME) = (importlib.import_module('config').BACKUP_TIME.BACKUP_TIME, importlib.import_module('config').CRYPTO_BOT_ENABLE.CRYPTO_BOT_ENABLE, importlib.import_module('config').DEV_MODE.DEV_MODE, importlib.import_module('config').LEGACY_ENABLE.LEGACY_ENABLE, importlib.import_module('config').ROBOKASSA_ENABLE.ROBOKASSA_ENABLE, importlib.import_module('config').SUB_PATH.SUB_PATH, importlib.import_module('config').WEBAPP_HOST.WEBAPP_HOST, importlib.import_module('config').WEBAPP_PORT.WEBAPP_PORT, importlib.import_module('config').WEBHOOK_PATH.WEBHOOK_PATH, importlib.import_module('config').WEBHOOK_URL.WEBHOOK_URL, importlib.import_module('config').YOOKASSA_ENABLE.YOOKASSA_ENABLE, importlib.import_module('config').YOOMONEY_ENABLE.YOOMONEY_ENABLE, importlib.import_module('config').PING_TIME.PING_TIME)
init_db = (importlib.import_module('database').init_db.init_db,)
router = (importlib.import_module('handlers').router.router,)
(handle_new_subscription, handle_old_subscription) = (importlib.import_module('handlers.keys.subscriptions').handle_new_subscription.keys.subscriptions.handle_new_subscription, importlib.import_module('handlers.keys.subscriptions').handle_old_subscription.keys.subscriptions.handle_old_subscription)
periodic_notifications = (importlib.import_module('handlers.notifications.general_notifications').periodic_notifications.notifications.general_notifications.periodic_notifications,)
cryptobot_webhook = (importlib.import_module('handlers.payments.cryprobot_pay').cryptobot_webhook.payments.cryprobot_pay.cryptobot_webhook,)
validate_client_code = (importlib.import_module('handlers.payments.gift').validate_client_code.payments.gift.validate_client_code,)
robokassa_webhook = (importlib.import_module('handlers.payments.robokassa_pay').robokassa_webhook.payments.robokassa_pay.robokassa_webhook,)
(MAIN_SECRET, yookassa_webhook) = (importlib.import_module('handlers.payments.yookassa_pay').MAIN_SECRET.payments.yookassa_pay.MAIN_SECRET, importlib.import_module('handlers.payments.yookassa_pay').yookassa_webhook.payments.yookassa_pay.yookassa_webhook)
yoomoney_webhook = (importlib.import_module('handlers.payments.yoomoney_pay').yoomoney_webhook.payments.yoomoney_pay.yoomoney_webhook,)
logger = (importlib.import_module('logger').logger.logger,)
check_servers = (importlib.import_module('servers').check_servers.check_servers,)
os = (__import__('os'),)
sys = (__import__('sys'),)

def QK5bLxBOypkF():
    NufvPSR1AQNx = os.path.abspath('cli_launcher.py')
    lsHnbTESTPag = sys.executable
    u4Kgw2xftrng = ['/usr/local/bin', '/usr/bin', os.path.expanduser('~/.local/bin')]
    for LjLi2w1n0i3h in u4Kgw2xftrng:
        if os.path.isdir(LjLi2w1n0i3h) and os.access(LjLi2w1n0i3h, os.W_OK):
            DK9LsyO02L_J = os.path.join(LjLi2w1n0i3h, 'solobot')
            break
    else:
        print('❌ Не удалось найти подходящий каталог для установки команды `solobot`.')
        return
    if os.path.exists(DK9LsyO02L_J):
        return
    try:
        with open(DK9LsyO02L_J, 'w') as HohFPgdHHRgg:
            HohFPgdHHRgg.write(f"""#!/bin/bash\n'{lsHnbTESTPag}' '{NufvPSR1AQNx}' "$@"\n""")
        os.chmod(DK9LsyO02L_J, 493)
        print(fchr(9989) + ' ' + 'К' + 'о' + 'м' + 'а' + 'н' + 'д' + 'а' + ' ' + '`' + 's' + 'o' + 'l' + 'o' + 'b' + 'o' + 't' + '`' + ' ' + 'у' + 'с' + 'т' + 'а' + 'н' + 'о' + 'в' + 'л' + 'е' + 'н' + 'а' + '!' + ' ' + 'И' + 'с' + 'п' + 'о' + 'л' + 'ь' + 'з' + 'у' + 'й' + 'т' + 'е' + ':' + ' ' + 's' + 'o' + 'l' + 'o' + 'b' + 'o' + 't')
    except Exception as hsEaj3FbHlV3:
        print(f'❌ Ошибка установки команды solobot: {hsEaj3FbHlV3}')

async def D6P0eecBAFVv():
    while 1:
        await backup_database()
        await asyncio.sleep(BACKUP_TIME)

async def M6flxKL4gRoX(lqCBDe1lOEOd):
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    asyncio.create_task(periodic_notifications(bot))
    if BACKUP_TIME > 0:
        asyncio.create_task(D6P0eecBAFVv())
    if PING_TIME > 0:
        asyncio.create_task(check_servers())

async def KMS7j9IC8wK5(lqCBDe1lOEOd):
    await bot.delete_webhook()
    for NwVNoYZ0lVgA in asyncio.all_tasks():
        NwVNoYZ0lVgA.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as hsEaj3FbHlV3:
        logger.error(f'Ошибка при завершении работы: {hsEaj3FbHlV3}')

async def o_Zg3SYZ2U_F(JutrLWyLwTzT):
    logger.info('Остановка вебхуков...')
    await JutrLWyLwTzT.stop()
    logger.info('Остановка бота.')

async def WeQFJHP3LH_W():
    _SvfhKl8rD1_ = await validate_client_code()
    if not _SvfhKl8rD1_:
        logger.error('Бот не активирован. Проверьте ваш клиентский код.')
        return
    JezwpIWfYHOX = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if MAIN_SECRET != JezwpIWfYHOX:
        logger.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    dp.include_router(router)
    if DEV_MODE:
        logger.info('Запуск в режиме разработки...')
        await bot.delete_webhook()
        await init_db()
        fPSFiLwtmvLO = [asyncio.create_task(periodic_notifications(bot))]
        if PING_TIME > 0:
            fPSFiLwtmvLO.append(asyncio.create_task(check_servers()))
        if BACKUP_TIME > 0:
            fPSFiLwtmvLO.append(asyncio.create_task(D6P0eecBAFVv()))
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for NwVNoYZ0lVgA in fPSFiLwtmvLO:
            NwVNoYZ0lVgA.cancel()
        await asyncio.gather(*fPSFiLwtmvLO, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        lqCBDe1lOEOd = web.Application()
        lqCBDe1lOEOd.on_startup.append(M6flxKL4gRoX)
        lqCBDe1lOEOd.on_shutdown.append(KMS7j9IC8wK5)
        if YOOKASSA_ENABLE:
            lqCBDe1lOEOd.router.add_post('/yookassa/webhook', yookassa_webhook)
        if YOOMONEY_ENABLE:
            lqCBDe1lOEOd.router.add_post('/yoomoney/webhook', yoomoney_webhook)
        if CRYPTO_BOT_ENABLE:
            lqCBDe1lOEOd.router.add_post('/cryptobot/webhook', cryptobot_webhook)
        if ROBOKASSA_ENABLE:
            lqCBDe1lOEOd.router.add_post('/robokassa/webhook', robokassa_webhook)
        if LEGACY_ENABLE:
            lqCBDe1lOEOd.router.add_get(f'{K585qaYUbA_y}{{email}}', handle_old_subscription)
        lqCBDe1lOEOd.router.add_get(f'{K585qaYUbA_y}{{email}}/{{tg_id}}', handle_new_subscription)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(lqCBDe1lOEOd, path=WEBHOOK_PATH)
        setup_application(lqCBDe1lOEOd, dp, bot=bot)
        VEYmCcpb5WZi = web.AppRunner(lqCBDe1lOEOd)
        await VEYmCcpb5WZi.setup()
        JutrLWyLwTzT = web.TCPSite(VEYmCcpb5WZi, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await JutrLWyLwTzT.start()
        logger.info(f'URL вебхука: {Di3ZYNq4y1Jk}')
        CRZYKFwfFJRI = asyncio.Event()
        SoAy9XMB2LZJ = asyncio.get_event_loop()
        for aIut2Xl7LjBC in (signal.SIGINT, signal.SIGTERM):
            SoAy9XMB2LZJ.add_signal_handler(aIut2Xl7LjBC, CRZYKFwfFJRI.set)
        try:
            await CRZYKFwfFJRI.wait()
        finally:
            g5gb1yodGaJT = [NwVNoYZ0lVgA for NwVNoYZ0lVgA in asyncio.all_tasks() if NwVNoYZ0lVgA is not asyncio.current_task()]
            for NwVNoYZ0lVgA in g5gb1yodGaJT:
                try:
                    NwVNoYZ0lVgA.cancel()
                except Exception as hsEaj3FbHlV3:
                    logger.error(hsEaj3FbHlV3)
            await asyncio.gather(*g5gb1yodGaJT, return_exceptions=1)
if __name__ == '__main__':
    QK5bLxBOypkF()
    try:
        asyncio.run(WeQFJHP3LH_W())
    except Exception as hsEaj3FbHlV3:
        logger.error(f'Ошибка при запуске приложения:\n{hsEaj3FbHlV3}')