from aiogram.utils.media_group import MediaGroupBuilder
from typing import Tuple, Any
import json


async def profile_display(user_data, for_edit: bool=False) -> Any:
    """
    Возвращает объект медиа-альбома для отображения профиля пользователя 
    во время оценки анкет или изменения профиля.

    :param user_data: Данные о пользователе.
    :param for_edit: Используется ли метод во время начала изменения профиля.
    """
    
    album_builder = MediaGroupBuilder(
        caption=f"{'Так выглядит ваша анкета:\n\n' if for_edit else ''}"\
        f"{user_data.name}, {user_data.age}, {user_data.city} "\
        f"{'' if user_data.description == 'None' else f'- {user_data.description}'}")
    
    for media_id in json.loads(user_data.media):
        album_builder.add_photo(media_id)

    return album_builder


async def media_album_builder(user_data: dict, description: str, state_record_media: bool) -> Tuple[str, Any]:
    """
    Возвращает json-объект со списком айдишников фото и объект медиа-альбома 
    для отображения профиля пользователя при окончании изменения профиля.
    
    :param user_data: Данные о пользователе.
    :param description: Описание пользователя.
    :param state_record_media: Изменяются ли фотографии.
    """

    media_album_id: list = []
    album_builder = MediaGroupBuilder(caption=f"{user_data['name']}, {user_data['age']}, {user_data['city']} "\
                                      f"{'' if description == 'None' else f'- {description}'}")
    if state_record_media:
        for media_id in json.loads(user_data['old_profile']['media']):
            album_builder.add_photo(media_id)
            media_album_id.append(media_id)
    else:
        for media_id in [user_data['media_1'], user_data['media_2'], user_data['media_3']]:
            if media_id != None:
                album_builder.add_photo(media_id)
                media_album_id.append(media_id)

    return (json.dumps(media_album_id), album_builder)


async def profile_display_admins(user_data, status_ban: bool) -> Any:
    """
    Возвращает объект медиа-альбома для отображения профиля пользователя 
    во время модерирования анкет админом.
    
    :param user_data: Данные пользователя.
    :param status_ban: Забанен ли пользователь
    """
    
    album_builder = MediaGroupBuilder(
        caption=f"ID: {user_data.telegram_id}\n\n"\
        f"{user_data.name}, {user_data.age}, {user_data.city} "\
        f"{'' if user_data.description == 'None' else f'- {user_data.description}'}\n\n"\
        f"@{user_data.user_name}, {'Мужчина🙍‍♂️' if user_data.gender == 'man' else 'Женщина🙍‍♀️'}\n"\
        f"Сатус профиля: {'активный🗣' if user_data.active_profile else 'неактивный💤'}\n"\
        f"Статус бана: {'забанен⚠️' if status_ban else 'не забанен🟢'}")
        
    for media_id in json.loads(user_data.media):
        album_builder.add_photo(media_id)

    return album_builder


async def profile_display_view_likes(user_data, message: str, count_likes: int=1) -> Any:
    """
    Возвращает объект медиа-альбома для отображения профиля пользователя 
    во время просмотра лайков.

    :param user_data: Данные о пользователе.
    :param message: Сообщениедля пользователя.
    :param count_like: Количесво лайков.
    """

    album_builder = MediaGroupBuilder(
        caption=f"Ваш профиль понравился{f' (еще {count_likes - 1})' if count_likes > 1 else ''}:\n\n"\
        f"{user_data.name}, {user_data.age}, {user_data.city} "\
        f"{'' if user_data.description == 'None' else f'- {user_data.description}'}"\
        f"{f'\n\nСообщение💌: {message}' if message != 'None' else ''}")
    
    for media_id in json.loads(user_data.media):
        album_builder.add_photo(media_id)

    return album_builder

