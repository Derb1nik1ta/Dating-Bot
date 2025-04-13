from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
import random
from typing import Optional, Union, Tuple, Any

from config.config import settings
from ...core.dictionary import *
from .search_kb import *
from .search_state import SearchState
from ...handlers.menu.menu_kb import menu_kb
from database.like_db import LikeUser
from database.profile_db import ProfileUser
from ...filters.check_like_limit import check_like_limit
from ...filters.check_ban import check_ban
from ...filters.chek_id import check_id
from ...filters.check_active import check_active_profile
from ...filters.validate_search import validate_message, validate_input_reason
from ...core.media_album_builder import profile_display
from ..menu.menu_state import MenuState

router_search = Router()


async def get_id_list_and_album(telegram_id: int, list_id_profiles: Optional[list]=None) -> Tuple[int, list, Any]:
    """
    Возвращает айди просматриваемого профиля, список айди, объект медиа-альбом для оценивания профиля.

    :param telegram_id: Телеграмм айди пользователя.
    :param list_id_profiles: Лист с айди профилей.
    """

    if list_id_profiles is None or len(list_id_profiles) == 0:
        profile_user = await ProfileUser.get_user_profile(telegram_id=telegram_id)
        list_id_profiles: list = await ProfileUser.get_profiles_assessment(gender=profile_user.gender)
        
        random.shuffle(list_id_profiles)
        if len(list_id_profiles) > 0:
            id_viewing_profile: int = list_id_profiles[0]
            viewing_profile = await ProfileUser.get_user_profile(telegram_id=int(id_viewing_profile))
            album_builder = await profile_display(user_data=viewing_profile)
        else:
            album_builder = None
            id_viewing_profile = None
    else:
        id_viewing_profile: int = list_id_profiles[0]
        viewing_profile = await ProfileUser.get_user_profile(telegram_id=id_viewing_profile)
        album_builder = await profile_display(user_data=viewing_profile)
    
    return (id_viewing_profile, list_id_profiles, album_builder)


async def get_message_for_send_like(id_viewing_profile: int) -> Tuple[int, str]:
    """
    Возвращает количество профилей, которые лайкнули пользователя и сообщения 
    для уведомления пользователя, что его профиль кому-то понравился.

    :param id_viewing_profile: Телеграмм айди просматриваемого пользователя.
    """

    data_likes: Union[None, Tuple[list, list]] = await LikeUser.get_like_user(telegram_id=id_viewing_profile)
    count_likes: int = 0 if data_likes == None else len(data_likes[0])
    profile = await ProfileUser.get_user_profile(telegram_id=id_viewing_profile)

    if profile.gender == 'man':
        gender_message: str = 'девушке, показать её?' if count_likes == 1 else 'девушкам, показать их?'
    else:
        gender_message: str = 'парню, показать его?' if count_likes == 1 else 'парням, показать их?'

    return (count_likes, gender_message)


@router_search.message(Command('search'))
@router_search.message(F.text == 'Поиск❤️')
@router_search.message(F.text == 'Продолжить поиск❤️', SearchState.continue_search)
async def start_search_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Начало просмтора профилей. Выводит пользователю профиль для оценки."""

    if await check_ban(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif not await check_id(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=validate_reg_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        await state.set_state(MenuState.menu)
    elif await check_active_profile(telegram_id=message.from_user.id ) == 'unactive':
        await bot.send_message(message.from_user.id, text=validate_active_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        await state.set_state(MenuState.menu)
    else:
        data: dict = await state.get_data()
        new_data = {k: v for k, v in data.items() if k in settings.NON_ERASABLE_REDIS_DATA}
        await state.set_data(data=new_data)

        if 'list_id_profiles' in data:
            id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(telegram_id=message.from_user.id, list_id_profiles=data['list_id_profiles'])
        else:
            id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(telegram_id=message.from_user.id)

        if id_viewing_profile is None:
            await bot.send_message(message.from_user.id, text=validate_search_message, reply_markup=await menu_kb(message.from_user.id))
        else:
            await state.update_data(data={'id_viewing_profile': id_viewing_profile, 'list_id_profiles': list_id_profiles})
            await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_assessment_kb())
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await state.set_state(SearchState.continue_search)


@router_search.callback_query(F.data == 'delete_likes')
async def delete_likes(callback: CallbackQuery, bot: Bot) -> None:
    """Удалить лайки. Очистка всех лайков у пользователя."""

    await LikeUser.clear_like_user(telegram_id=callback.from_user.id)
    await bot.send_message(callback.from_user.id, 'Лайки удалены')
    await callback.message.delete()
    await callback.answer()


@router_search.callback_query(F.data == 'view_likes_later')
async def view_likes_later(callback: CallbackQuery) -> None:
    """Просмотр лайков позже. Удаляет сообщение с уведомлением."""

    await callback.message.delete()
    await callback.answer()


@router_search.message(F.text == '❤️', SearchState.continue_search)
@router_search.message(F.text == '👎', SearchState.continue_search)
@router_search.message(F.text == '👈Назад', SearchState.input_message)
@router_search.message(F.text == '👈Назад', SearchState.input_reason)
async def continue_search_profile(message: Message, bot: Bot, state:FSMContext) -> None:
    """Продолжение оценки профилей. Выводит пользователю профиль для оценки."""

    if await check_ban(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        data: dict  = await state.get_data()
        if message.text == '👈Назад':
            viewing_profile = await ProfileUser.get_user_profile(telegram_id=data['id_viewing_profile'])
            album_builder = await profile_display(user_data=viewing_profile)

            await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_assessment_kb())
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await state.set_state(SearchState.continue_search)
        elif message.text == '👎' or message.text == '❤️':
            if new_data := await check_like_limit(data):
                if message.text == '❤️':
                    id_viewing_profile: int = data['id_viewing_profile']
                    state_adding_like: Optional[bool] = await LikeUser.add_like_user(telegram_id=message.from_user.id, telegram_id_like=id_viewing_profile)
                    count_likes, gender_message = await get_message_for_send_like(id_viewing_profile=id_viewing_profile)
                    if state_adding_like:
                        try:
                            await bot.send_message(id_viewing_profile, text=f'Твой профиль понравился {count_likes} {gender_message}', reply_markup=await view_likes_kb())
                        except TelegramForbiddenError:
                            await ProfileUser.update_user_active(telegram_id=id_viewing_profile, state_active=False)

                data['list_id_profiles'].pop(0)
                id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(telegram_id=message.from_user.id, list_id_profiles=data['list_id_profiles'])
                await state.update_data(data={'id_viewing_profile': id_viewing_profile, 'list_id_profiles': list_id_profiles,
                                              'count_like': new_data['count_like'], 'first_like_time': new_data['first_like_time']})
                await bot.send_media_group(message.from_user.id, media=album_builder.build())
            else:
                await bot.send_message(message.from_user.id, text=validate_like_message, reply_markup=await menu_kb(message.from_user.id))
                await state.set_state(MenuState.menu)


@router_search.message(F.text == '💌', SearchState.continue_search)
async def input_message_search_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод текста для сообщения пользователю."""

    data: dict = await state.get_data()
    if new_data := await check_like_limit(data):
        await state.update_data(data={'count_like': new_data['count_like'], 'first_like_time': new_data['first_like_time']})
        await bot.send_message(message.from_user.id, text=input_text_message, reply_markup=await return_menu_kb())
        await state.set_state(SearchState.input_message)
    else:
        await bot.send_message(message.from_user.id, text=validate_like_message, reply_markup=await menu_kb(message.from_user.id))
        await state.set_state(MenuState.menu)


@router_search.message(SearchState.input_message)
async def finish_input_search_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Отправка сообщения пользователю. Продолжение поиска"""

    if await validate_message(str(message.text)):
        await bot.send_message(message.from_user.id, text=validate_input_message)
    else:
        data: dict = await state.get_data()
        id_viewing_profile: int = data['id_viewing_profile']

        state_adding_like: Optional[bool] = await LikeUser.add_like_user(telegram_id=message.from_user.id, telegram_id_like=id_viewing_profile, message=str(message.text))
        count_likes, gender_message = await get_message_for_send_like(id_viewing_profile=id_viewing_profile)
        if state_adding_like:
            try: 
                await bot.send_message(id_viewing_profile, text=f'Твой профиль понравился {count_likes} {gender_message}', reply_markup=await view_likes_kb())
            except TelegramForbiddenError:
                profile_db = ProfileUser()
                await profile_db.update_user_active(telegram_id=id_viewing_profile, state_active=False)

        data['list_id_profiles'].pop(0)
        id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(telegram_id=message.from_user.id, list_id_profiles=data['list_id_profiles'])
        await state.update_data(data={'id_viewing_profile': id_viewing_profile, 'list_id_profiles': list_id_profiles})
        await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_assessment_kb())
        await bot.send_media_group(message.from_user.id, media=album_builder.build())
        await state.set_state(SearchState.continue_search)


@router_search.message(F.text == 'Пожаловаться⚠️', SearchState.continue_search)
async def input_reason_complaint(message: Message, bot: Bot, state: FSMContext):
    """Ввод текста причины жалобы."""

    await bot.send_message(message.from_user.id, text=input_reason_complaint_message, reply_markup=await return_menu_kb())
    await state.set_state(SearchState.input_reason)

@router_search.message(SearchState.input_reason)
async def send_complaint(message: Message, bot: Bot, state: FSMContext):
    """Отправка жалобы в чат с жалобами."""

    if await validate_input_reason(str(message.text)):
        data: dict = await state.get_data()

        text_complain = f'Пользователь ID: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a> '\
                        f'пожаловался на ID: <a href="tg://user?id={data['id_viewing_profile']}">{data['id_viewing_profile']}</a> \n\n'\
                        f'Причина жалобы: {message.text}'
        for_pin = await bot.send_message(chat_id=settings.ID_GROUP_COMPLAINT, text=text_complain)
        await bot.pin_chat_message(chat_id=settings.ID_GROUP_COMPLAINT, message_id=for_pin.message_id)

        data['list_id_profiles'].pop(0)
        id_viewing_profile, list_id_profiles, album_builder = await get_id_list_and_album(telegram_id=message.from_user.id, list_id_profiles=data['list_id_profiles'])
        await state.update_data(data={'id_viewing_profile': id_viewing_profile, 'list_id_profiles': list_id_profiles})
        await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_assessment_kb())
        await bot.send_media_group(message.from_user.id, media=album_builder.build())
        await state.set_state(SearchState.continue_search)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_reason_message)
