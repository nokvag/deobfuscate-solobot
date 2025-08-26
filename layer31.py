from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from handlers.keys.subscriptions import handle_new_subscription, handle_old_subscription
from handlers.notifications.general_notifications import periodic_notifications
from handlers.payments.cryprobot_pay import cryptobot_webhook
from handlers.payments.gift import validate_client_code
from handlers.payments.robokassa_pay import robokassa_webhook
from handlers.payments.yookassa_pay import MAIN_SECRET, yookassa_webhook
from handlers.payments.yoomoney_pay import yoomoney_webhook

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
        print('✅ Команда `solobot` установлена! Используйте: solobot')
    except Exception as exc:
        print(f'❌ Ошибка установки команды solobot: {exc}')

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
        logger.error(f'Ошибка при завершении работы: {exc}')

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
            app.router.add_get(f'{SUB_PATH}{{email}}', handle_old_subscription)
        app.router.add_get(f'{SUB_PATH}{{email}}/{{tg_id}}', handle_new_subscription)
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host=WEBAPP_HOST, port=WEBAPP_PORT)
        await site.start()
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
                except Exception as exc:
                    logger.error(exc)
            await asyncio.gather(*pending, return_exceptions=1)
if __name__ == '__main__':
    install_cli()
    try:
        asyncio.run(main())
    except Exception as exc:
        logger.error(f'Ошибка при запуске приложения:\n{exc}')