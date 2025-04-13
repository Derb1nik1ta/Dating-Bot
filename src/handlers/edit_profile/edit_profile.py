from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from typing import Optional, Union

from ...core.media_album_builder import media_album_builder, profile_display
from ...handlers.menu.menu_kb import menu_kb
from .edit_profile_kb import *
from ...core.dictionary import *
from ...filters.validate_edit import *
from .edit_profile_state import EditProfileState
from database.profile_db import ProfileUser
from ...filters.check_active import check_active_profile
from ...filters.check_ban import check_ban
from ..menu.menu_state import MenuState

router_edit = Router()



@router_edit.message((F.text == 'Откл профиль💤') | (F.text == 'Вкл профиль🗣'))
async def edit_active_profile(message: Message, bot: Bot, state: FSMContext) -> None:
    """Изменение видимости профиля для других пользователей."""

    if await check_ban(message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        active_profile: Union[str, bool] = await check_active_profile(message.from_user.id)
        if active_profile == 'active':
            await ProfileUser.update_user_active(telegram_id=message.from_user.id, state_active=False)
            await bot.send_message(message.from_user.id, text=profile_unactive_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        elif active_profile == 'unactive':
            await ProfileUser.update_user_active(telegram_id=message.from_user.id, state_active=True)
            await bot.send_message(message.from_user.id, text=profile_active_message, reply_markup=await menu_kb(telegram_id=message.from_user.id))
        else:
            await bot.send_message(message.from_user.id, text=validate_reg_message)
        await state.set_state(MenuState.menu)


@router_edit.message(Command('edit'))
@router_edit.message(Command('reg'))
@router_edit.message((F.text == 'Заполнить анкету✍') | (F.text == 'Изменить анкету✍'))
async def input_gender(message: Message, bot: Bot, state: FSMContext) -> None:
    """Выбор пола."""

    if await check_ban(message.from_user.id):
        await bot.send_message(message.from_user.id, text=ban_message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        profile = await ProfileUser.get_user_profile(message.from_user.id)
        if profile != None:
            profile_user_message = await profile_display(user_data=profile, for_edit=True)
            await bot.send_media_group(message.from_user.id, media=profile_user_message.build())

            profile: dict = {
                'gender': profile.gender,
                'name': profile.name,
                'age': profile.age,
                'city': profile.city,
                'description': profile.description,
                'media': profile.media
            }

        await state.update_data(old_profile=profile)
        await bot.send_message(message.from_user.id, text=input_gender_message, reply_markup=await gender_kb())
        await state.set_state(EditProfileState.input_gender_state)


@router_edit.message(EditProfileState.input_gender_state)
async def input_name(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод имени."""

    if await validate_gender(str(message.text)):
        user_data: dict = await state.get_data()
        await state.update_data(gender='man' if message.text == 'Мужской ♂' else 'woman')
        await bot.send_message(message.from_user.id, text=input_name_message, reply_markup=await name_kb(user_data['old_profile']))
        await state.set_state(EditProfileState.input_name_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_gender_message)


@router_edit.message(EditProfileState.input_name_state)
async def input_age(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод возраста."""

    if await validate_name(str(message.text)):
        user_data: dict = await state.get_data()
        await state.update_data(name=message.text)
        await bot.send_message(message.from_user.id, text=input_age_message, reply_markup=await age_kb(user_data['old_profile']))
        await state.set_state(EditProfileState.input_age_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_name_message)


@router_edit.message(EditProfileState.input_age_state)
async def input_city(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод названия города."""

    if await validate_age(str(message.text)):
        user_data: dict = await state.get_data()
        await state.update_data(age=int(message.text))
        await bot.send_message(message.from_user.id, text=input_city_message, reply_markup=await city_kb(user_data['old_profile']))
        await state.set_state(EditProfileState.input_city_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_age_message)


@router_edit.message(EditProfileState.input_city_state)
async def input_description(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод описания."""

    if await validate_city(str(message.text)):
        user_data: dict = await state.get_data()
        await state.update_data(city=message.text)
        await bot.send_message(message.from_user.id, text=input_description_message, reply_markup=await description_kb(user_data['old_profile']))
        await state.set_state(EditProfileState.input_description_state)
    else:
        await bot.send_message(message.from_user.id, text=validate_city_message)


@router_edit.message(EditProfileState.input_description_state)
async def input_media_1(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод первой фотографии."""

    if message.text in ('Не изменять✅', 'Без описания📝') or await validate_description(str(message.text)):
        user_data: dict = await state.get_data()
        if message.text == 'Не изменять✅':
            await state.update_data(description=user_data['old_profile']['description'])
        else:
            description: str = 'None' if message.text == 'Без описания📝' else str(message.text)
            await state.update_data(description=description)
        await bot.send_message(message.from_user.id, text=input_media_message % ('1'), reply_markup=await media_kb_1(user_data['old_profile']))
        await state.set_state(EditProfileState.input_media_state_1)
    else:
        await bot.send_message(message.from_user.id, text=validate_description_message)


@router_edit.message(F.text == 'Не изменять✅', EditProfileState.input_media_state_1)
@router_edit.message(F.text == 'Оставить 1📷', EditProfileState.input_media_state_2)
@router_edit.message(EditProfileState.input_media_state_3)
async def results(message: Message, bot: Bot, state: FSMContext) -> None:
    """Запись данных в базу данных и показ измененной анкеты."""

    if message.photo or message.text in ('Оставить 1📷', 'Оставить 2📷', 'Не изменять✅'):
        if message.photo:
            await state.update_data(media_3=message.photo[-1].file_id)
        
        user_data: dict = await state.get_data()

        list_state = ['adm_id_viewing_profile', 'adm_list_id_profiles', 'count_like', 'first_like_time']
        if user_data['old_profile'] and user_data['old_profile']['gender'] == user_data['gender']:
            list_state.extend(('id_viewing_profile', 'list_id_profiles'))
        new_data = {k: v for k, v in user_data.items() if k in list_state}
        await state.set_data(data=new_data)

        media_id, album_builder = await media_album_builder(user_data=user_data, description=user_data['description'], \
                                                            state_record_media=True if message.text == 'Не изменять✅' else False)
        if await ProfileUser.get_user_profile(telegram_id=message.from_user.id) == None:
            state_record: bool = await ProfileUser.add_user_profile(
                telegram_id=message.from_user.id,
                user_name=message.from_user.username,
                gender=user_data['gender'],
                name=user_data['name'],
                age=user_data['age'],
                city=user_data['city'],
                description=user_data['description'],
                media=media_id)
        else:
            state_record: bool = await ProfileUser.update_user_profile(
                telegram_id=message.from_user.id,
                user_name=message.from_user.username,
                gender=user_data['gender'],
                name=user_data['name'],
                age=user_data['age'],
                city=user_data['city'],
                description=user_data['description'],
                media=media_id)

        if state_record:
            await bot.send_media_group(message.from_user.id, media=album_builder.build())
            await bot.send_message(message.from_user.id, text=finish_input_message, reply_markup=await menu_kb(message.from_user.id))
        else:
            await bot.send_message(message.from_user.id, text=validate_record_message, reply_markup=await menu_kb(message.from_user.id))
        await state.set_state(MenuState.menu)
    else:
        await bot.send_message(message.from_user.id, text=validate_media_message)


@router_edit.message(EditProfileState.input_media_state_1)
async def input_media_2(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод второй фотографии."""

    if message.photo:
        await state.update_data(media_1=message.photo[-1].file_id, media_2=None, media_3=None)
        await bot.send_message(message.from_user.id, text=input_media_message % ('2'), reply_markup=await media_kb_2())
        await state.set_state(EditProfileState.input_media_state_2)
    else:
        await bot.send_message(message.from_user.id, text=validate_media_message)


@router_edit.message(EditProfileState.input_media_state_2)
async def input_media_3(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ввод третьей фотографии."""

    if message.photo:
        await state.update_data(media_2=message.photo[-1].file_id)
        await bot.send_message(message.from_user.id, text=input_media_message % ('3'), reply_markup=await media_kb_3())
        await state.set_state(EditProfileState.input_media_state_3)
    else:
        await bot.send_message(message.from_user.id, text=validate_media_message)
