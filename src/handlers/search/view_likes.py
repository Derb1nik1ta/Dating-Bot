from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from typing import Optional, Union, Tuple

from config.config import settings
from ...core.dictionary import *
from .search_kb import *
from .search_state import SearchState
from ...handlers.menu.menu_kb import menu_kb
from database.like_db import LikeUser
from database.profile_db import ProfileUser
from ...filters.check_ban import check_ban
from ...filters.chek_id import check_id
from ...filters.validate_search import validate_input_reason
from ...core.media_album_builder import profile_display_view_likes
from .search import get_message_for_send_like
from ..menu.menu_state import MenuState


router_view_likes = Router()


@router_view_likes.callback_query(F.data == 'view_likes')
async def view_likes(callback: CallbackQuery, state: FSMContext) -> None:
    """Начало просмотра лайков через уведомление. Выводит пользователю профиль для оценки."""

    if await check_ban(telegram_id=callback.from_user.id):
        await callback.message.answer(text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif not await check_id(telegram_id=callback.from_user.id):
        await callback.message.answer(text=validate_reg_message, reply_markup=await menu_kb(telegram_id=callback.from_user.id))
        await state.set_state(MenuState.menu)
    else:
        likes: Union[None, Tuple[str, str]] = await LikeUser.get_like_user(telegram_id=callback.from_user.id)
        if likes == None:
            await callback.message.answer(text=validate_view_likes_message, reply_markup=await menu_kb(telegram_id=callback.from_user.id))
            await state.set_state(MenuState.menu)
        else:
            list_likes: list = likes[0]
            list_message: list = likes[1]
            id_like: int = int(list_likes[0][1:] if list_likes[0][0] == 'm' else list_likes[0])

            profile = await ProfileUser.get_user_profile(telegram_id=id_like)

            album_builder = await profile_display_view_likes(user_data=profile, message=list_message[0], count_likes=len(list_likes))
            await state.set_state(SearchState.view_likes)
            
            if list_likes[0][0] == 'm':
                await callback.message.answer(text=start_search_message, reply_markup=await profile_mutual_like_kb(state_mutual=True))
                await callback.message.answer_media_group(media=album_builder.build())
                await callback.message.answer(text=mutual_like_message, 
                                reply_markup=await link_profile_kb(telegram_id=id_like))
                list_likes.pop(0)
                list_message.pop(0)
            else:
                await callback.message.answer(text=start_search_message, reply_markup=await profile_mutual_like_kb())
                await callback.message.answer_media_group(media=album_builder.build())
            await state.update_data(data={'mutual_list_likes': list_likes, 'mutual_list_message': list_message, 'mutual_id_like': id_like})
    await callback.message.delete()
    await callback.answer()


@router_view_likes.message(F.text == 'Мои лайки💘')
async def view_likes(message: Message, bot: Bot, state: FSMContext) -> None:
    """Начало просмотра лайков через меню. Выводит пользователю профиль для оценки."""

    if await check_ban(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    elif not await check_id(telegram_id=message.from_user.id):
        await bot.send_message(message.from_user.id, text=validate_reg_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        await state.set_state(MenuState.menu)
    else:
        likes: Union[None, Tuple[list, list]] = await LikeUser.get_like_user(telegram_id=message.from_user.id)
        if likes == None:
            await bot.send_message(message.from_user.id, text=validate_view_likes_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
            await state.set_state(MenuState.menu)
        else:
            list_likes: list = likes[0]
            list_message: list = likes[1]
            id_like: int = int(list_likes[0][1:] if list_likes[0][0] == 'm' else list_likes[0])

            profile = await ProfileUser.get_user_profile(telegram_id=int(id_like))

            album_builder = await profile_display_view_likes(user_data=profile, message=list_message[0], count_likes=len(list_likes))
            
            if list_likes[0][0] == 'm':
                await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_mutual_like_kb(state_mutual=True))
                await bot.send_media_group(message.from_user.id, media=album_builder.build())
                await bot.send_message(message.from_user.id, text=mutual_like_message, 
                                reply_markup=await link_profile_kb(telegram_id=id_like))
                list_likes.pop(0)
                list_message.pop(0)
                await LikeUser.remove_like_user(telegram_id=message.from_user.id)
            else:
                await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_mutual_like_kb())
                await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await state.update_data(data={'mutual_list_likes': list_likes, 'mutual_list_message': list_message, 'mutual_id_like': id_like})
            await state.set_state(SearchState.view_likes)
                
                
@router_view_likes.message(F.text == 'Продолжить❤️', SearchState.view_likes)
@router_view_likes.message(F.text == '💞', SearchState.view_likes)
@router_view_likes.message(F.text == '👎', SearchState.view_likes)
@router_view_likes.message(F.text == '👈Назад', SearchState.view_likes_input_reason)
async def assessment_viewed_likes(message: Message, bot: Bot, state: FSMContext) -> None:
    """Продолжение просмотра лайков. Выводит пользователю профиль для оценки."""

    data: dict = await state.get_data()
    list_likes: list = data['mutual_list_likes']
    list_message: list = data['mutual_list_message']
    id_like: int = data['mutual_id_like']

    if message.text == '💞':
        state_adding_like: Optional[bool] = await LikeUser.add_like_user(
            telegram_id=message.from_user.id,
            telegram_id_like=id_like,
            mutual_like=True)

        await bot.send_message(message.from_user.id, text=mutual_like_message, 
                                reply_markup=await link_profile_kb(telegram_id=id_like))

        count_likes, gender_message = await get_message_for_send_like(id_viewing_profile=id_like)
        if state_adding_like:
            try: 
                await bot.send_message(id_like, text=f'Твой профиль понравился {count_likes} {gender_message}', reply_markup=await view_likes_kb())
            except TelegramForbiddenError:
                await ProfileUser.update_user_active(telegram_id=id_like, state_active=False)
    
    if message.text == '💞' or message.text == '👎':
        list_likes.pop(0)
        list_message.pop(0)
        await LikeUser.remove_like_user(telegram_id=message.from_user.id)
    
    if len(list_likes) > 0:
        id_like: int = int(list_likes[0][1:] if list_likes[0][0] == 'm' else list_likes[0])
        profile = await ProfileUser.get_user_profile(telegram_id=int(id_like))
        album_builder = await profile_display_view_likes(user_data=profile, message=list_message[0], count_likes=len(list_likes))
        if list_likes[0][0] == 'm':
            await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_mutual_like_kb(state_mutual=True))
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await bot.send_message(message.from_user.id, text=mutual_like_message, 
                                reply_markup=await link_profile_kb(telegram_id=id_like))
            list_likes.pop(0)
            list_message.pop(0)
            await LikeUser.remove_like_user(telegram_id=message.from_user.id)
        else:
            await bot.send_message(message.from_user.id, text=start_search_message, reply_markup=await profile_mutual_like_kb())
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
        await state.update_data(data={'mutual_list_likes': list_likes, 'mutual_list_message': list_message, 'mutual_id_like': id_like})
    else:
        new_data = {k: v for k, v in data.items() if k in settings.NON_ERASABLE_REDIS_DATA}
        await state.set_data(data=new_data)
        await bot.send_message(message.from_user.id, text=completing_likes_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        await state.clear()


@router_view_likes.message(F.text == 'Пожаловаться⚠️', SearchState.view_likes)
async def input_reason_complaint(message: Message, bot: Bot, state: FSMContext):
    """Ввод текста причины жалобы."""

    await bot.send_message(message.from_user.id, text=input_reason_complaint_message, reply_markup=await return_menu_kb())
    await state.set_state(SearchState.view_likes_input_reason)


@router_view_likes.message(SearchState.view_likes_input_reason)
async def send_complaint(message: Message, bot: Bot, state: FSMContext):
    """Отправка жалобы в чат с жалобами."""

    if await validate_input_reason(str(message.text)):
        data: dict = await state.get_data()
        list_likes: list = data['mutual_list_likes']
        list_message: list = data['mutual_list_message']
        id_like: int = data['mutual_id_like']

        text_complain = f'Пользователь ID: <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a> '\
                        f'пожаловался на ID: <a href="tg://user?id={id_like}">{id_like}</a> \n\n'\
                        f'Причина жалобы: {message.text}'
        for_pin = await bot.send_message(chat_id=settings.ID_GROUP_COMPLAINT, text=text_complain)
        await bot.pin_chat_message(chat_id=settings.ID_GROUP_COMPLAINT, message_id=for_pin.message_id)

        if str(id_like) in list_likes or 'm' + str(id_like) in list_likes:
            list_likes.pop(0)
            list_message.pop(0)
            await LikeUser.remove_like_user(telegram_id=message.from_user.id)

        await state.update_data(data={'mutual_list_likes': list_likes, 'mutual_list_message': list_message})
        await bot.send_message(message.from_user.id, text=complain_successful_delivered_message, reply_markup=await successful_delivered_complain_kb())
        await state.set_state(SearchState.view_likes)
    else:
        await bot.send_message(message.from_user.id, text=validate_input_reason_message)
