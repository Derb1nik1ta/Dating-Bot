from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ...filters.check_owner import check_owner
from ...filters.check_ban import check_ban

async def menu_admins_kb(telegram_id: int) -> ReplyKeyboardMarkup:
    """
    Кнопки для меню модераторов.
    
    :param telegram_id: Телеграмм айди пользователя.
    """

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Забанить🔨'))
    builder.add(KeyboardButton(text='Разбанить⭐'))
    builder.add(KeyboardButton(text='Просмотр анкет👮‍♀️'))
    builder.add(KeyboardButton(text='Найти анкету🕵️‍♂️'))
    builder.add(KeyboardButton(text='Отправить💬'))
    builder.add(KeyboardButton(text='Получить баны⚠️'))
    builder.add(KeyboardButton(text='Меню🗒️'))
    if await check_owner(telegram_id=telegram_id):
        builder.add(KeyboardButton(text='Вперед👉'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def return_menu_kb() -> ReplyKeyboardMarkup:
    """
    Кнопки для возрата в меню или меню модерации."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Модерация⚙️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def search_admins_kb(telegram_id: int) -> ReplyKeyboardMarkup:
    """
    Кнопки для модерирования анкет.
    
    :param telegram_id: Телеграмм айди пользователя.
    """

    builder = ReplyKeyboardBuilder()
    
    if await check_ban(telegram_id=telegram_id):
        builder.add(KeyboardButton(text='Разбанить⭐'))
    else:
        builder.add(KeyboardButton(text='Забанить🔨'))
    builder.add(KeyboardButton(text='Отправить💬'))
    builder.add(KeyboardButton(text='Модерация⚙️'))
    builder.add(KeyboardButton(text='Продолжить🕵️‍♂️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def return_menu_search_kb() -> ReplyKeyboardMarkup:
    """Кнопки для возрата действия или в меню или меню модерации во время модерирования анкет."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='👈Назад'))
    builder.add(KeyboardButton(text='Модерация⚙️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard