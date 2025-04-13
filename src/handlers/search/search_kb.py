from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def profile_assessment_kb() -> ReplyKeyboardMarkup:
    """Кнопки для оценки профилей."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='💌'))
    builder.add(KeyboardButton(text='❤️'))
    builder.add(KeyboardButton(text='👎'))
    builder.add(KeyboardButton(text='Пожаловаться⚠️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(3)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def profile_mutual_like_kb(state_mutual: bool=False) -> ReplyKeyboardMarkup:
    """
    Кнопки для оценивания профилей с взаимной симпатией.
    
    :param state_mutual: Взаимная ли любовь.
    """

    builder = ReplyKeyboardBuilder()

    if state_mutual:
        builder.add(KeyboardButton(text='Продолжить❤️'))

    else:
        builder.add(KeyboardButton(text='💞'))
        builder.add(KeyboardButton(text='👎'))
        
    builder.add(KeyboardButton(text='Пожаловаться⚠️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def successful_delivered_complain_kb() -> ReplyKeyboardMarkup:
    """Кнопки после написания причины жалобы."""

    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Продолжить❤️'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def link_profile_kb(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Инлайн-кнопка с сыллкой на профиль телеграмм.

    :param telegram_id: Телеграмм айди пользователя.
    """

    button_url: str = f'tg://user?id={telegram_id}'
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f'Ссылка на профиль🔗', url=button_url))

    return builder.as_markup()


async def view_likes_kb() -> InlineKeyboardMarkup:
    """Инлайн-кнопки для сообшения пользователю, что его профиль кому-то понравился."""

    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(
        text='Да👍',
        callback_data='view_likes'))
    builder.add(InlineKeyboardButton(
        text='Позже💤',
        callback_data='view_likes_later'))
    builder.add(InlineKeyboardButton(
        text='Удалить лайки🙅‍♂️',
        callback_data='delete_likes'))
    builder.adjust(2)
    return builder.as_markup()


async def return_menu_kb() -> ReplyKeyboardMarkup:
    """Кнопки во время ввода текста для жалобы или сообщения."""
    
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='👈Назад'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard

