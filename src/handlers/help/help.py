from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from config.config import settings
from ...core.dictionary import help_message, ban_message
from ...handlers.menu.menu_kb import menu_kb
from ...filters.check_ban import check_ban
from ..menu.menu_state import MenuState
from .help_kb import help_kb

router_help = Router()

@router_help.message(Command('help'))
@router_help.message(F.text == 'Помощь🆘')
async def menu(message: Message, bot: Bot, state: FSMContext) -> None:
    """Выводит текст для решения проблем пользователя."""
    
    if await check_ban(message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        user_data: dict = await state.get_data()
        new_data = {k: v for k, v in user_data.items() if k in settings.NON_ERASABLE_REDIS_DATA}
        await state.set_data(data=new_data)
        
        await bot.send_message(message.from_user.id, text=help_message, reply_markup=await menu_kb(message.from_user.id))
        await state.set_state(MenuState.menu)
