from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from typing import Optional

from ...core.date_now import get_date_now
from ...core.loggers import admins_logger
from ...core.dictionary import *
from ...core.media_album_builder import profile_display_admins
from ...filters.check_admin import check_admin
from ...filters.check_owner import check_owner
from ...filters.chek_id import check_id
from ...filters.check_ban import check_ban
from ...filters.validate_admins import *
from .admins_menu_kb import menu_admins_kb, return_menu_kb
from .states_menu_admins import AdminsState, OwnersState
from ...handlers.menu.menu_kb import menu_kb
from database.bans_db import BansUser
from database.profile_db import ProfileUser


router_admins = Router()


@router_admins.message(F.text == 'Модерация⚙️')
@router_admins.message(F.text == '👈Назад', OwnersState.menu_owners_state)
async def menu_admins(message: Message, bot: Bot, state: FSMContext) -> None:
    """Меню модераторов."""

    if await check_ban(message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif await check_admin(telegram_id=message.from_user.id) or await check_owner(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=menu_admins_message, reply_markup=await menu_admins_kb(telegram_id=message.from_user.id))
        await state.set_state(AdminsState.menu_admins_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_admin_message)


@router_admins.message(F.text == 'Забанить🔨', AdminsState.menu_admins_state)
async def inp_id_get_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для выдачи бана пользователю."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(AdminsState.inp_id_get_ban_state)


@router_admins.message(AdminsState.inp_id_get_ban_state)
async def inp_reason_get_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод причины бана."""

    if not await validate_input_id(str(message.text)):
        await bot.send_message(message.from_user.id, text=validate_input_id_message)
    elif not await check_id(int(message.text)):
        await bot.send_message(message.from_user.id, text=validate_search_profile_message)
    elif await check_ban(int(message.text)):
        await bot.send_message(message.from_user.id, text=validate_get_ban_message)
    elif await check_admin(int(message.text)) or await check_owner(int(message.text)):
        await bot.send_message(message.from_user.id, text=validate_ban_admin_message)
    else:
        await state.update_data(telegram_id=int(message.text))
        await bot.send_message(message.from_user.id, text=input_reason_message)
        await state.set_state(AdminsState.inp_reason_get_ban_state)


@router_admins.message(AdminsState.inp_reason_get_ban_state)
async def get_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Запись бана в бд и отправка уведомления пользователю о его бане."""

    if await validate_input_reason(str(message.text)):
        data: dict = await state.get_data()
        await BansUser.add_ban_user(telegram_id=data['telegram_id'], admin_id=message.from_user.id, reason=str(message.text))
        await ProfileUser.update_user_active(telegram_id=data['telegram_id'], state_active=False)
        try:
            ban_message_: str = f'Вы были забанены по причине🔒: {message.text}\n\n'\
                        f'Оспорить бан: <a href="{settings.LINK_GROUP_HELP}">Чат поддержки🧰</a>'
            await bot.send_message(data['telegram_id'], text=ban_message_, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
        except TelegramForbiddenError: pass
        
        await bot.send_message(message.from_user.id, text=get_ban_message, reply_markup=await menu_admins_kb(telegram_id=message.from_user.id))
        await state.set_state(AdminsState.menu_admins_state)
       
        admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} banned id_user={data['telegram_id']} for reason: {message.text}")
    else:
        await bot.send_message(message.from_user.id, text=validate_input_reason_message)


@router_admins.message(F.text == 'Разбанить⭐', AdminsState.menu_admins_state)
async def inp_id_delete_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для разбана пользователя."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(AdminsState.inp_id_delete_ban_state)


@router_admins.message(AdminsState.inp_id_delete_ban_state)
async def delete_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Удаление бана с бд и отправка уведомления пользователю о его разбане."""

    if await validate_input_id(telegram_id=str(message.text)):
        if await BansUser.delete_ban_user(telegram_id=int(message.text)):
            try:
                await bot.send_message(message.text, text=unban_message, reply_markup=await menu_kb(message.text))
                await ProfileUser.update_user_active(telegram_id=int(message.text), state_active=True)
            except TelegramForbiddenError: pass
            await bot.send_message(message.from_user.id, text=delete_ban_message, reply_markup=await menu_admins_kb(telegram_id=message.from_user.id))

            admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} unbanned id_user={message.text}")
        else:
            await bot.send_message(message.from_user.id, text=validate_delete_ban_message)
        await state.set_state(AdminsState.menu_admins_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_id_message)


@router_admins.message(F.text == 'Отправить💬', AdminsState.menu_admins_state)
async def inp_id_send_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для отправки уведомления пользователю."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(AdminsState.inp_id_send_message_state)


@router_admins.message(AdminsState.inp_id_send_message_state)
async def inp_text_send_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод сообщения для отправки уведомления пользователю."""

    if not await validate_input_id(telegram_id=str(message.text)):
        await bot.send_message(message.from_user.id, text=validate_input_id_message)
    elif not await check_id(telegram_id=int(message.text)):
        await bot.send_message(message.from_user.id, text=validate_search_profile_message)
    else:
        await state.update_data(telegram_id=int(message.text))
        await bot.send_message(message.from_user.id, text=input_text_message)
        await state.set_state(AdminsState.inp_text_send_message_state)
        

@router_admins.message(AdminsState.inp_text_send_message_state)
async def send_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка уведомления пользователю от модератора."""

    if await validate_input_text(text=str(message.text)):
        data: dict = await state.get_data()
        try:
            await bot.send_message(data['telegram_id'], text=f'admin: {message.text}', disable_web_page_preview=True)
            await bot.send_message(message.from_user.id, text=message_successful_delivered_message, reply_markup=await menu_admins_kb(message.from_user.id))
            admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} sent for id_user={data['telegram_id']} message: {message.text}")
        except TelegramForbiddenError:
            await ProfileUser.update_user_active(telegram_id=data['telegram_id'], state_active=False)
            await bot.send_message(message.from_user.id, text=validate_send_message, reply_markup=await menu_admins_kb(telegram_id=message.from_user.id))
        await state.set_state(AdminsState.menu_admins_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_text_message)


@router_admins.message(F.text == 'Найти анкету🕵️‍♂️', AdminsState.menu_admins_state)
async def inp_id_search_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод айди для поиска анкеты пользователя."""

    await bot.send_message(message.from_user.id, text=input_id_message, reply_markup=await return_menu_kb())
    await state.set_state(AdminsState.inp_id_search_profile_state)


@router_admins.message(AdminsState.inp_id_search_profile_state)
async def search_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка модератору анкеты пользователя."""

    if await validate_input_id(str(message.text)):
        profile_user = await ProfileUser.get_user_profile(telegram_id=int(message.text))
        if profile_user is None:
            await bot.send_message(message.from_user.id, text=validate_search_profile_message, reply_markup=await menu_admins_kb(message.from_user.id))
        else:
            status_ban: bool = await check_ban(telegram_id=message.text)
            album_builder = await profile_display_admins(user_data=profile_user, status_ban=status_ban)
            await bot.send_message(message.from_user.id, text='Так выглядит профиль:', reply_markup=await menu_admins_kb(message.from_user.id))
            await bot.send_media_group(message.from_user.id, media=album_builder.build())

            admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} search profile id_user={message.text}")
        await state.set_state(AdminsState.menu_admins_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_id_message)


@router_admins.message(F.text == 'Получить баны⚠️', AdminsState.menu_admins_state)
async def get_bans(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка модератору сообщение о данных всех банов"""

    info_bans: Optional[str] = await BansUser.get_ban_users()
    await bot.send_message(message.from_user.id, text=str(info_bans), reply_markup=await menu_admins_kb(message.from_user.id))
    await state.set_state(AdminsState.menu_admins_state)

    admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} got data all bans.")
