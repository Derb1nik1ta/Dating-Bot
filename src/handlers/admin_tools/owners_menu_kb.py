from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def menu_owners_kb() -> ReplyKeyboardMarkup:
    """Кнопки меню владельца."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Дать админку⚙️'))
    builder.add(KeyboardButton(text='Забрать админку⭐'))
    builder.add(KeyboardButton(text='Рассылка💬'))
    builder.add(KeyboardButton(text='Айди админов🧲'))
    builder.add(KeyboardButton(text='Логги🧑‍💻'))
    builder.add(KeyboardButton(text='Получить стату📊'))
    builder.add(KeyboardButton(text='👈Назад'))
    
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def return_menu_kb() -> ReplyKeyboardMarkup:
    """Кнопки для возрата в меню или меню модерации."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Модерация⚙️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard
