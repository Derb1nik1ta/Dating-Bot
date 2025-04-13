from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
import logging
import asyncio

from src.handlers.start.start import router_start
from src.handlers.edit_profile.edit_profile import router_edit
from src.handlers.menu.menu import router_menu
from src.handlers.help.help import router_help
from src.handlers.search.search import router_search
from src.handlers.search.view_likes import router_view_likes
from src.handlers.admin_tools.admins_menu import router_admins
from src.handlers.admin_tools.owners_menu import router_owner
from src.handlers.admin_tools.admins_search import router_admins_search

from database.Database import DataBase
from config.config import settings


async def set_commands() -> None:
    """Устананавливает команды для бота."""

    commands: list = [BotCommand(command='menu', description='Меню🗒️'),
                BotCommand(command='search', description='Поиск❤️'),
                BotCommand(command='help', description='Помощь🆘'),]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot() -> None:
    """Отправляет сообщение владельцу о запуске бота."""

    await set_commands()
    await bot.send_message(settings.ID_OWNER, '🤖Бот запустился!')


async def stop_bot():
    """Отправляет сообщение владельцу о завершение рабоыт бота."""

    await bot.send_message(settings.ID_OWNER, '🤖Бот выключился!')


async def main() -> None:
    """Главная функция. Используется для настройки и запуска бота."""
    
    # with Redis
    # storage = RedisStorage.from_url(url=settings.get_url_redis())

    # without Redis
    storage = None

    # create db
    await DataBase.create_db()
    # logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=storage)
    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    # регистрация роутеров
    dp.include_routers(router_start, router_menu, router_help, router_search, router_view_likes, 
                       router_edit, router_admins, router_admins_search, router_owner, )
    try:
        # не пропускаем сообщения для отключенного бота
        await bot.delete_webhook(drop_pending_updates=True)
        # запуск бота
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    bot = Bot(token=settings.get_bot_token(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main())
