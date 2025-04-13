from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from ...core.dictionary import start_message, ban_message
from ...handlers.menu.menu_kb import menu_kb
from ...filters.check_ban import check_ban
from ..menu.menu_state import MenuState

router_start = Router()

@router_start.message(Command('start'))
async def start_bot(message: Message, bot: Bot, state: FSMContext) -> None:
    """Приветствует новых пользователей."""
    
    if await check_ban(message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id, text=start_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        await state.set_state(MenuState.menu)
