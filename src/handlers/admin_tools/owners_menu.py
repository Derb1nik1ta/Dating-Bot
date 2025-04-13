from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
import asyncio
from typing import Optional

from ...core.date_now import get_date_now
from ...core.dictionary import *
from ...core.loggers import owner_logger
from .owners_menu_kb import menu_owners_kb, return_menu_kb
from .states_menu_admins import AdminsState, OwnersState
from ...handlers.menu.menu_kb import menu_kb
from ...filters.check_owner import check_owner
from ...filters.validate_admins import validate_input_id
from database.admin_db import AdminUser
from database.profile_db import ProfileUser


router_owner = Router()


@router_owner.message(F.text == 'Вперед👉', AdminsState.menu_admins_state)
async def menu_admins(message: Message, bot: Bot, state: FSMContext) -> None:
    """Меню владельца."""

    if await check_owner(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=menu_owners_message, reply_markup=await menu_owners_kb())
        await state.set_state(OwnersState.menu_owners_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_admin_message)


@router_owner.message(F.text == 'Дать админку⚙️', OwnersState.menu_owners_state)
async def inp_id_get_admin(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для выдачи админки пользователю."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(OwnersState.inp_id_get_admin_state)


@router_owner.message(OwnersState.inp_id_get_admin_state)
async def get_admin(message: Message, bot: Bot, state: FSMContext) -> None:
    """Запись айди админа в бд."""

    if await validate_input_id(str(message.text)):
        if await AdminUser.add_admin_user(int(message.text)):
            await bot.send_message(message.from_user.id, text=get_admin_message, reply_markup=await menu_owners_kb())
            await state.set_state(OwnersState.menu_owners_state)
            owner_logger.info(f"{await get_date_now()} - owner gave admin to user_id={message.text}")
        else:
            await bot.send_message(message.from_user.id, text=validate_get_admin_message)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_id_message)


@router_owner.message(F.text == 'Забрать админку⭐', OwnersState.menu_owners_state)
async def inp_id_delete_admin(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для удаления админки у пользователя."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(OwnersState.inp_id_delete_admin_state)


@router_owner.message(OwnersState.inp_id_delete_admin_state)
async def delete_admin(message: Message, bot: Bot, state: FSMContext) -> None:
    """Удаление админки с бд."""

    if await validate_input_id(str(message.text)) and not await check_owner(int(message.text)):
        if await AdminUser.delete_admin_user(int(message.text)):
            await bot.send_message(message.from_user.id, text=delete_admin_message, reply_markup=await menu_owners_kb())
            await state.set_state(OwnersState.menu_owners_state)
            owner_logger.info(f"{await get_date_now()} - owner deleted admin from user_id={message.text}")
        else:
            await bot.send_message(message.from_user.id, text=validate_delete_admin_message)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_id_message)


@router_owner.message(F.text == 'Рассылка💬', OwnersState.menu_owners_state)
async def inp_text_everyone_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод сообщения для рассылки всем пользователям."""

    await bot.send_message(message.from_user.id, text=input_text_send_everyone_message, reply_markup=await return_menu_kb())
    await state.set_state(OwnersState.inp_text_for_send_everyone_state)

@router_owner.message(OwnersState.inp_text_for_send_everyone_state)
async def send_everyone_message(message: Message, bot: Bot, state: FSMContext):
    """Рассылка сообщения всем пользователям."""

    all_id: Optional[list] = await ProfileUser.get_all_id()

    iteration: int = 0
    for telegram_id in all_id:
        if iteration > 25:
            await asyncio.sleep(2)
            iteration: int = 0
        try:
            await bot.send_message(telegram_id, text=message.text, disable_web_page_preview=True)
            iteration += 1
        except TelegramForbiddenError:
            await ProfileUser.update_user_active(telegram_id=telegram_id, state_active=False)
        except Exception as error:
            print(f'[+] ID: {telegram_id}, error: {error}')
    
    await bot.send_message(message.from_user.id, text=message_successful_delivered_messages, reply_markup=await menu_owners_kb())
    await state.set_state(OwnersState.menu_owners_state)
    owner_logger.info(f"{await get_date_now()} - owner sent everyone message: {message.text[:20]}...")


@router_owner.message(F.text == 'Айди админов🧲', OwnersState.menu_owners_state)
async def get_id_admins(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка айди всех админов владельцу."""

    id_admins: Optional[list] = await AdminUser.get_admin_users()
    await bot.send_message(message.from_user.id, text=f'Админы: {', '.join(id_admins)}' if len(id_admins) > 0 else 'Админов нету в бд✖️', reply_markup=await menu_owners_kb())
    await state.set_state(OwnersState.menu_owners_state)
    owner_logger.info(f"{await get_date_now()} - owner gоt id admins")


@router_owner.message(F.text == 'Логги🧑‍💻', OwnersState.menu_owners_state)
async def get_logs_admins(message: Message, bot: Bot) -> None:
    """Отправка файлов с логгами владельцу."""

    await bot.send_document(message.from_user.id, document=FSInputFile(path='database\\logging_files\\01_admins.log'))
    await bot.send_document(message.from_user.id, document=FSInputFile(path='database\\logging_files\\01_owner.log'))
    await bot.send_document(message.from_user.id, document=FSInputFile(path='database\\logging_files\\01_error_db.log'))
    owner_logger.info(f"{await get_date_now()} - owner got logs")


@router_owner.message(F.text == 'Получить стату📊', OwnersState.menu_owners_state)
async def get_statistics(message: Message, bot: Bot) -> None:
    """Отправка статистики бота владельцу"""

    statistics: Optional[dict] = await ProfileUser.get_statistics()

    text_statistics: str = f'👤Всего анкет: {statistics['count_profile']}\n'\
           f'👨Мужских: {statistics['count_man']}\n'\
           f'👩Женских: {statistics['count_woman']}\n'\
           f'🗣Активных: {statistics['count_active_profile']}\n'\
           f'💤Неактивных: {statistics['count_unactive_profile']}\n\n'\
           f'📆Средний возраст: {round(statistics['average_age'], 2)}\n'\
           f'🙍‍♂️Средний возраст: {round(statistics['average_age_man'], 2)}\n'\
           f'🙍‍♀️Средний возраст: {round(statistics['average_age_woman'], 2)}\n\n'\
           f'🥇Популярное имя: {statistics['most_common_name']}\n'
              
    await bot.send_message(message.from_user.id, text=text_statistics)
    owner_logger.info(f"{await get_date_now()} - owner got bot statistics")
