from aiogram import F, Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
import random
from typing import Optional, Tuple, Any

from ...core.media_album_builder import profile_display_admins
from ...core.date_now import get_date_now
from ...core.loggers import admins_logger
from config.config import settings
from ...core.dictionary import *
from ...filters.check_ban import check_ban
from ...filters.check_admin import check_admin
from ...filters.check_owner import check_owner
from ...filters.validate_admins import *
from database.profile_db import ProfileUser
from database.bans_db import BansUser
from .states_menu_admins import AdminsSearchState, AdminsState
from .admins_menu_kb import *
from ...handlers.menu.menu_kb import menu_kb


router_admins_search = Router()


async def get_id_list_and_album(list_id_profiles: Optional[list]=None) -> Tuple[int, list, Any]:
    """
    Возвращает айди просматриваемого профиля, список айди, объект медиа-альбом для модерирования профиля.

    :param list_id_profiles: Лист с айди профилей.
    """

    if list_id_profiles is None or len(list_id_profiles) == 0:
        list_id_profiles: Optional[list] = await ProfileUser.get_all_id()
        random.shuffle(list_id_profiles)

    id_viewing_profiles: int = list_id_profiles[0]
        
    viewing_profile = await ProfileUser.get_user_profile(telegram_id=id_viewing_profiles)
    album_builder = await profile_display_admins(user_data=viewing_profile, status_ban=await check_ban(telegram_id=id_viewing_profiles))
    return (id_viewing_profiles, list_id_profiles, album_builder)


@router_admins_search.message(F.text == 'Просмотр анкет👮‍♀️', AdminsState.menu_admins_state)
async def start_admins_search(message: Message, bot: Bot, state: FSMContext) -> None:
    """Начало просмотра анкет для модерирования. Выводит модератору анкету."""

    data: dict = await state.get_data()
    if 'adm_list_id_profiles' in data:
        adm_id_viewing_profile, adm_list_id_profiles, adm_album_builder = await get_id_list_and_album(data['adm_list_id_profiles'])
    else:
        adm_id_viewing_profile, adm_list_id_profiles, adm_album_builder = await get_id_list_and_album()
    await state.update_data(adm_id_viewing_profile=adm_id_viewing_profile, adm_list_id_profiles=adm_list_id_profiles)
    await bot.send_message(message.from_user.id, text=search_admins_message, reply_markup=await search_admins_kb(telegram_id=adm_id_viewing_profile))
    await bot.send_media_group(message.from_user.id, media=adm_album_builder.build())
    await state.set_state(AdminsSearchState.continue_search)

    admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} moderates profiles")


@router_admins_search.message(F.text == '👈Назад', AdminsSearchState.inp_text_send_message)
@router_admins_search.message(F.text == '👈Назад', AdminsSearchState.inp_reason_ban)
@router_admins_search.message(AdminsSearchState.continue_search)
async def continue_admins_search(message: Message, bot: Bot, state: FSMContext) -> None:
    """
    Обрабатывает действия модераторов.
    
    Кнопки:
    👈Назад - отменяет действие.
    Отправить💬 - запрашивает текст у модератора для отправки уведомления.
    Забанить🔨 - запрашивает причину бана у модератора.
    Разбанить⭐ - снимает бан с пользователя.
    Продолжить🕵️‍♂️ - показывает следующую анкету для модерирования.
    """

    match message.text:
        case '👈Назад':
            data: dict = await state.get_data()
            viewing_profile: int = await ProfileUser.get_user_profile(telegram_id=data['adm_id_viewing_profile'])
            album_builder = await profile_display_admins(user_data=viewing_profile, status_ban=await check_ban(telegram_id=data['adm_id_viewing_profile']))

            await bot.send_message(message.from_user.id, text=search_admins_message, reply_markup=await search_admins_kb(telegram_id=data['adm_id_viewing_profile']))
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await state.set_state(AdminsSearchState.continue_search)
        case 'Отправить💬':
            await bot.send_message(message.from_user.id, text=input_text_message, reply_markup=await return_menu_search_kb())
            await state.set_state(AdminsSearchState.inp_text_send_message)

        case 'Забанить🔨':
            data: dict = await state.get_data()
            if await check_ban(data['adm_id_viewing_profile']):
                await bot.send_message(message.from_user.id, text=validate_get_ban_message)
            elif await check_admin(data['adm_id_viewing_profile']) or await check_owner(data['adm_id_viewing_profile']):
                await bot.send_message(message.from_user.id, text=validate_ban_admin_message)
            else:
                await bot.send_message(message.from_user.id, text=input_reason_message, reply_markup=await return_menu_search_kb())
                await state.set_state(AdminsSearchState.inp_reason_ban)

        case 'Разбанить⭐':
            data: dict = await state.get_data()
            if await BansUser.delete_ban_user(telegram_id=data['adm_id_viewing_profile']):
                try:
                    await bot.send_message(data['adm_id_viewing_profile'], text=unban_message, reply_markup=await menu_kb(data['adm_id_viewing_profile']))
                    await ProfileUser.update_user_active(telegram_id=data['adm_id_viewing_profile'], state_active=True)
                except TelegramForbiddenError: pass

                await bot.send_message(message.from_user.id, text=delete_ban_message, reply_markup=await search_admins_kb(telegram_id=data['adm_id_viewing_profile']))
                admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} unbanned id_user={data['adm_id_viewing_profile']}")
            else:
                await bot.send_message(message.from_user.id, text=validate_delete_ban_message)

        case 'Продолжить🕵️‍♂️':
            data: dict = await state.get_data()
            data['adm_list_id_profiles'].pop(0)
            id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(list_id_profiles=data['adm_list_id_profiles'])
            await state.update_data(adm_id_viewing_profile=id_viewing_profile, adm_list_id_profiles=list_id_profiles)
            # await bot.send_message(message.from_user.id, text=search_admins_message, reply_markup=await search_admins_kb(telegram_id=id_viewing_profile))
            await bot.send_media_group(message.from_user.id, media=album_builder.build())


@router_admins_search.message(AdminsSearchState.inp_text_send_message)
async def send_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка уведомления пользователю от модератора."""

    if await validate_input_text(text=str(message.text)):
        data: dict = await state.get_data()
        try:
            await bot.send_message(data['adm_id_viewing_profile'], text=f'admin: {message.text}')
            await bot.send_message(message.from_user.id, text=message_successful_delivered_message, reply_markup=await search_admins_kb(telegram_id=data['adm_id_viewing_profile']))
        except TelegramForbiddenError:
            profile_db = ProfileUser()
            await profile_db.update_user_active(telegram_id=data['adm_id_viewing_profile'], state_active=False)
            await bot.send_message(message.from_user.id, text=validate_send_message, reply_markup=await search_admins_kb(telegram_id=data['adm_id_viewing_profile']))

        await state.set_state(AdminsSearchState.continue_search)
        admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} sent for id_user={data['adm_id_viewing_profile']} message: {message.text}")
    else:
        await bot.send_message(message.from_user.id, text=validate_input_text_message)


@router_admins_search.message(AdminsSearchState.inp_reason_ban)
async def get_ban(message: Message, bot: Bot, state: FSMContext) -> None:
    """Запись бана в бд и отправка уведомления пользователю о его бане."""

    if await validate_input_reason(str(message.text)):
        data: dict = await state.get_data()
        await BansUser.add_ban_user(telegram_id=data['adm_id_viewing_profile'], admin_id=message.from_user.id, reason=message.text)
        await ProfileUser.update_user_active(telegram_id=data['adm_id_viewing_profile'], state_active=False)
        try:
            ban_message_: str = f'Вы были забанены по причине🔒: {message.text}\n\n'\
                        f'Оспорить бан: <a href="{settings.LINK_GROUP_HELP}">Чат поддержки🧰</a>'
            await bot.send_message(data['adm_id_viewing_profile'], text=ban_message_, reply_markup=ReplyKeyboardRemove())
        except TelegramForbiddenError: pass
        
        await bot.send_message(message.from_user.id, text=get_ban_message, reply_markup=await search_admins_kb(telegram_id=data['adm_id_viewing_profile']))
        await state.set_state(AdminsSearchState.continue_search)
       
        admins_logger.info(f"{await get_date_now()} - id_admin={message.from_user.id} banned id_user={data['adm_id_viewing_profile']} for reason: {message.text}")
    else:
        await bot.send_message(message.from_user.id, text=validate_input_reason_message)
    