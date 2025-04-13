from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.config import settings

async def help_kb() -> InlineKeyboardMarkup:
    """Инлайн-кнопка с чатом поддержки."""
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f'Чат поддержки🔗', url=settings.LINK_GROUP_HELP))
    return builder.as_markup()