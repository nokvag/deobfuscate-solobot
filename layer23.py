from bot import bot, dp
from config import BACKUP_TIME, CRYPTO_BOT_ENABLE, DEV_MODE, LEGACY_ENABLE, ROBOKASSA_ENABLE, SUB_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL, YOOKASSA_ENABLE, YOOMONEY_ENABLE, PING_TIME
from aiohttp import web
from backup import backup_database
from database import init_db
from handlers import router
from servers import check_servers
import asyncio
import logger
import os
import signal
import sys
import importlib
(SimpleRequestHandler, setup_application) = (importlib.import_module('aiogram.webhook.aiohttp_server').SimpleRequestHandler.webhook.aiohttp_server.SimpleRequestHandler, importlib.import_module('aiogram.webhook.aiohttp_server').setup_application.webhook.aiohttp_server.setup_application)
(handle_new_subscription, handle_old_subscription) = (importlib.import_module('handlers.keys.subscriptions').handle_new_subscription.keys.subscriptions.handle_new_subscription, importlib.import_module('handlers.keys.subscriptions').handle_old_subscription.keys.subscriptions.handle_old_subscription)
periodic_notifications = (importlib.import_module('handlers.notifications.general_notifications').periodic_notifications.notifications.general_notifications.periodic_notifications,)
cryptobot_webhook = (importlib.import_module('handlers.payments.cryprobot_pay').cryptobot_webhook.payments.cryprobot_pay.cryptobot_webhook,)
validate_client_code = (importlib.import_module('handlers.payments.gift').validate_client_code.payments.gift.validate_client_code,)
robokassa_webhook = (importlib.import_module('handlers.payments.robokassa_pay').robokassa_webhook.payments.robokassa_pay.robokassa_webhook,)
(MAIN_SECRET, yookassa_webhook) = (importlib.import_module('handlers.payments.yookassa_pay').MAIN_SECRET.payments.yookassa_pay.MAIN_SECRET, importlib.import_module('handlers.payments.yookassa_pay').yookassa_webhook.payments.yookassa_pay.yookassa_webhook)
yoomoney_webhook = (importlib.import_module('handlers.payments.yoomoney_pay').yoomoney_webhook.payments.yoomoney_pay.yoomoney_webhook,)

def install_cli():
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
    except Exception as exc:
        print(f'❌ Ошибка установки команды solobot: {err}')

async def backup_loop():
    while 1:
        await backup_database()
        await asyncio.sleep(BACKUP_TIME)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    await init_db()
    asyncio.create_task(periodic_notifications(bot))
    if BACKUP_TIME > 0:
        asyncio.create_task(backup_loop())
    if PING_TIME > 0:
        asyncio.create_task(check_servers())

async def on_shutdown(app):
    await bot.delete_webhook()
    for task in asyncio.all_tasks():
        task.cancel()
    try:
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=1)
    except Exception as exc:
        logger.error(f'Ошибка при завершении работы: {err}')

async def stop_webhooks(site):
    logger.info('Остановка вебхуков...')
    await site.stop()
    logger.info('Остановка бота.')

async def main():
    is_valid_code = await validate_client_code()
    if not is_valid_code:
        logger.error('Бот не активирован. Проверьте ваш клиентский код.')
        return
    expected_secret = 'SOLO-ACCESS-KEY-B4TN-92QX-L7ME'
    if MAIN_SECRET != expected_secret:
        logger.error('Нарушена целостность файлов! Обновитесь с полной заменой папки!')
        return
    dp.include_router(router)
    if DEV_MODE:
        logger.info('Запуск в режиме разработки...')
        await bot.delete_webhook()
        await init_db()
        bg_tasks = [asyncio.create_task(periodic_notifications(bot))]
        if PING_TIME > 0:
            bg_tasks.append(asyncio.create_task(check_servers()))
        if BACKUP_TIME > 0:
            bg_tasks.append(asyncio.create_task(backup_loop()))
        await dp.start_polling(bot)
        logger.info('Polling остановлен в режиме разработки. Отмена фоновых задач...')
        for task in bg_tasks:
            task.cancel()
        await asyncio.gather(*bg_tasks, return_exceptions=1)
    else:
        logger.info('Запуск в production режиме...')
        app = web.Application()
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
        if LEGACY_ENABLE:
            app.router.add_get(f'{K585qaYUbA_y}{{email}}', handle_old_subscription)
        app.router.add_get(f'{K585qaYUbA_y}{{email}}/{{tg_id}}', handle_new_subscription)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await site.start()
        logger.info(f'URL вебхука: {Di3ZYNq4y1Jk}')
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
    install_cli()
    try:
        asyncio.run(main())
    except Exception as exc:
        logger.error(f'Ошибка при запуске приложения:\n{err}')