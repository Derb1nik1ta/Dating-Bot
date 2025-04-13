from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from ...filters.check_admin import check_admin
from ...filters.check_owner import check_owner
from ...filters.chek_id import check_id
from ...filters.check_active import check_active_profile


async def menu_kb(telegram_id: int) -> ReplyKeyboardMarkup:
    """
    Кнопки для меню.
    
    :param telegram_id: Телеграмм айди пользователя.
    """
    
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text='Поиск❤️'))
    if await check_id(telegram_id=telegram_id):
        builder.add(KeyboardButton(text='Изменить анкету✍'))
        builder.add(KeyboardButton(text='Мои лайки💘'))
    else:
        builder.add(KeyboardButton(text='Заполнить анкету✍'))
    
    active_profile = await check_active_profile(telegram_id=telegram_id)
    if active_profile == 'active':
        builder.add(KeyboardButton(text='Откл профиль💤'))
    elif active_profile == 'unactive':
        builder.add(KeyboardButton(text='Вкл профиль🗣'))
    
    builder.add(KeyboardButton(text='Помощь🆘'))

    if await check_admin(telegram_id=telegram_id) or await check_owner(telegram_id=telegram_id):
        builder.add(KeyboardButton(text='Модерация⚙️'))

    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True)
    return keyboard
