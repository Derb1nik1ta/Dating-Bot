from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Optional


async def gender_kb() -> ReplyKeyboardMarkup:
    """Кнопки для выбора пола."""

    gender_kb_: list = [
        [KeyboardButton(text='Мужской ♂'), KeyboardButton(text='Женский ♀')],
        [KeyboardButton(text='Меню🗒️')]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=gender_kb_, resize_keyboard=True)
    return keyboard


async def name_kb(profile: Optional[dict]) -> ReplyKeyboardMarkup:
    """
    Кнопки во время ввода имени.
    
    :param profile: Словарь с данными пользователя.
    """

    builder = ReplyKeyboardBuilder()
    if profile != None:
        builder.add(KeyboardButton(text=profile['name']))
    builder.add(KeyboardButton(text='Меню🗒️'))

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def age_kb(profile: Optional[dict]) -> ReplyKeyboardMarkup:
    """
    Кнопки во время ввода возраста.
    
    :param profile: Словарь с данными пользователя.
    """
    
    builder = ReplyKeyboardBuilder()
    if profile != None:
        builder.add(KeyboardButton(text=str(profile['age'])))
    builder.add(KeyboardButton(text='Меню🗒️'))

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def city_kb(profile: Optional[dict]) -> ReplyKeyboardMarkup:
    """
    Кнопки во время ввода города.
    
    :param profile: Словарь с данными пользователя.
    """
    
    builder = ReplyKeyboardBuilder()
    if profile != None:
        builder.add(KeyboardButton(text=profile['city']))
    builder.add(KeyboardButton(text='Меню🗒️'))

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def description_kb(profile: Optional[dict]) -> ReplyKeyboardMarkup:
    """
    Кнопки во время ввода описания.
    
    :param profile: Словарь с данными пользователя.
    """
    
    builder = ReplyKeyboardBuilder()
    if profile != None:
        builder.add(KeyboardButton(text='Не изменять✅'))
    builder.add(KeyboardButton(text='Без описания📝'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    builder.adjust(2)

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard


async def media_kb_1(profile: Optional[dict]) -> ReplyKeyboardMarkup:
    """
    Кнопки во время ввода первой фотографии.
    
    :param profile: Словарь с данными пользователя.
    """
    
    builder = ReplyKeyboardBuilder()
    if profile != None:
        builder.add(KeyboardButton(text='Не изменять✅'))
    builder.add(KeyboardButton(text='Меню🗒️'))

    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard

async def media_kb_2() -> ReplyKeyboardMarkup:
    """Кнопки во время ввода второй фотографии."""
    
    media_kb_ = [[KeyboardButton(text='Оставить 1📷'),
        KeyboardButton(text='Меню🗒️')]]

    keyboard = ReplyKeyboardMarkup(keyboard=media_kb_, resize_keyboard=True)
    return keyboard

async def media_kb_3() -> ReplyKeyboardMarkup:
    """Кнопки во время ввода третьей фотографии."""
    
    media_kb_ = [[KeyboardButton(text='Оставить 2📷'),
        KeyboardButton(text='Меню🗒️')]]

    keyboard = ReplyKeyboardMarkup(keyboard=media_kb_, resize_keyboard=True)
    return keyboard
