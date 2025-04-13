from sqlalchemy import select
from .models import Like
from .Database import DataBase
import json
from src.core.date_now import get_date_now
from src.core.loggers import error_logger
from typing import Optional, Union, Tuple


class LikeUser(DataBase):
    """Класс для взаимодействия с таблицей Like."""
    @classmethod
    async def add_like_user(cls, telegram_id: int, telegram_id_like: int, message: Optional[str]='None', mutual_like: bool=False) -> Optional[bool]:
        """
        Добавляет пользователя в таблицу Like.

        :param telegram_id: Телеграмм айди пользователя.
        :param telegram_id_like: Телеграмм айди пользователя, которого лайкнули.
        :param message: Сообщение для пользователя.
        :param mutual_like: Взаимная любовь или нет.     
        """
        
        try:
            async with cls.Session() as request:
                profile_like = await cls.get_obj_like_user(telegram_id=telegram_id_like)

                telegram_id_res: str = str(telegram_id) if not mutual_like else 'm' + str(telegram_id)
                if profile_like == None:
                    list_like: list = [telegram_id_res]
                    list_message: list = [str(message)]
                    request.add(Like(
                        telegram_id=telegram_id_like,
                        like=json.dumps(list_like),
                        message=json.dumps(list_message, ensure_ascii=False),
                    ))
                    await request.commit()
                    return True
                else:
                    list_liked_: list = json.loads(profile_like.like)
                    list_message_: list = json.loads(profile_like.message)

                    mutual_like_id: str = 'm' + str(telegram_id)

                    if (str(telegram_id) not in list_liked_ and mutual_like_id not in list_liked_):
                        list_liked_.append(telegram_id_res)
                        list_message_.append(str(message))

                        profile_like.like = json.dumps(list_liked_)
                        profile_like.message = json.dumps(list_message_, ensure_ascii=False)
                        request.add(profile_like)
                        await request.commit()
                        return True
                    elif (mutual_like and str(telegram_id) in list_liked_ and mutual_like_id not in list_liked_) or \
                        (str(telegram_id) in list_liked_ and list_message_[list_liked_.index(str(telegram_id))] == 'None'):

                        index_like: int = list_liked_.index(str(telegram_id))
                        list_liked_.pop(index_like)
                        list_message_.pop(index_like)

                        list_liked_.append(telegram_id_res)
                        list_message_.append(str(message))

                        profile_like.like = json.dumps(list_liked_)
                        profile_like.message = json.dumps(list_message_, ensure_ascii=False)
                        request.add(profile_like)
                        await request.commit()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error adding like: [+] {error}")

    @classmethod
    async def get_obj_like_user(cls, telegram_id: int):
        """
        Возвращает скалярный объект пользователя с его данными с таблицы Like.
        
        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                user_like = await request.execute(select(Like).where(Like.telegram_id==telegram_id))
            return user_like.scalar()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting object likes: [+] {error}")
    
    @classmethod
    async def get_like_user(cls, telegram_id: int) -> Union[None, Tuple[list, list]]:
        """
        Возвращает данные пользователя с таблицы Like.
        
        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            profile_like = await cls.get_obj_like_user(telegram_id=telegram_id)

            if profile_like == None or profile_like.like == '[]':
                return None
            else:
                list_liked: list = json.loads(profile_like.like)
                list_message: list = json.loads(profile_like.message)
                return (list_liked, list_message)
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting likes: [+] {error}")
    
    @classmethod
    async def remove_like_user(cls, telegram_id: int) -> None:
        """
        Удаляет первый лайк и сообщение у пользователя.

        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                profile_like = await cls.get_obj_like_user(telegram_id=telegram_id)

                list_like: list = json.loads(profile_like.like)
                list_message: list = json.loads(profile_like.message)

                if len(list_like) > 0:
                    list_like.pop(0)
                    list_message.pop(0)

                    profile_like.like = json.dumps(list_like)
                    profile_like.message = json.dumps(list_like, ensure_ascii=False)

                    request.add(profile_like)
                    await request.commit()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error deletion like: [+] {error}")

    @classmethod
    async def clear_like_user(cls, telegram_id: int) -> None:
        """
        Очищает списки с лайкми и сообщениями у пользователя.

        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                profile_like = await cls.get_obj_like_user(telegram_id=telegram_id)

                if profile_like != None or profile_like.like != '[]':
                    profile_like.like = '[]'
                    profile_like.message = '[]'

                    request.add(profile_like)
                    await request.commit()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error clearing likes: [+] {error}")
