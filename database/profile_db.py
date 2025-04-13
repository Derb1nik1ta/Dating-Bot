from sqlalchemy import select
from .models import Users
from .Database import DataBase
from statistics import mode as most_common
from src.core.date_now import get_date_now
from src.core.loggers import error_logger
from typing import Optional

class ProfileUser(DataBase):
    """Класс для взаимодействия с таблицей Profile."""
    @classmethod
    async def add_user_profile(cls, telegram_id: int, user_name: str, gender: str, name: str, age: int, city: str, description: str, media: str) -> bool:
        """
        Добавляет пользователя в таблицу Profile.
        
        :param telegram_id: Телеграмм айди пользователя.
        :param user_name: Юзернейм пользователя в телеграмм.
        :param gender: Пол пользователя.
        :param name: Имя пользователя.
        :param age: Возраст пользователя.
        :param city: Город пользователя.
        :param description: Описание пользователя.
        :param media: json-объект со списком айдишников фотографий.
        """
        
        try:
            async with cls.Session() as request:
                request.add(Users(
                    telegram_id=telegram_id,
                    user_name=user_name,
                    gender=gender,
                    name=name,
                    age=age,
                    city=city,
                    description=description,
                    media=media
                ))
                await request.commit()
            return True
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 10] - error adding profile: [+] {error}")
            return False

    @classmethod
    async def update_user_profile(cls, telegram_id: int, user_name: str, gender: str, name: str, age: int, city: str, description: str, media: str) -> bool:
        """
        Обновление данных пользователя в таблице Profile.
        
        :param telegram_id: Телеграмм айди пользователя.
        :param user_name: Юзернейм пользователя в телеграмм.
        :param gender: Пол пользователя.
        :param name: Имя пользователя.
        :param age: Возраст пользователя.
        :param city: Город пользователя.
        :param description: Описание пользователя.
        :param media: json-объект со списком айдишников фотографий.
        """

        try:
            async with cls.Session() as request:
                user_profile = await cls.get_user_profile(telegram_id=telegram_id)
                
                user_profile.user_name = user_name
                user_profile.gender = gender
                user_profile.name = name
                user_profile.age = age
                user_profile.city = city
                user_profile.description = description
                user_profile.media = media

                request.add(user_profile)
                await request.commit()  
            return True  
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 30] - error updating profile: [+] {error}")
            return False
        
    @classmethod
    async def get_profiles_assessment(cls, gender: str) -> Optional[list]:
        """
        Возвращает профили для оценки с таблицы Profile.
        
        :param gender: Пол пользователя.
        """

        try:
            async with cls.Session() as request:
                gender_search: str = 'man' if gender == 'woman' else 'woman'
                profiles = await request.execute(select(Users).where(Users.gender==gender_search and Users.active_profile == True))
                
                id_profiles: list = []
                for profile in profiles.scalars().all():
                    id_profiles.append(profile.telegram_id)
            return id_profiles
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 51] - error getting id profiles for assessment: [+] {error}")

    @classmethod
    async def get_user_profile(cls, telegram_id: int) -> None:
        """
        Возвращает данные пользователя с таблицы Profile.
        
        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                result = await request.execute(select(Users).where(Users.telegram_id==telegram_id))
            return result.scalar()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 66] - error getting profile: [+] {error}")
        
    @classmethod
    async def update_user_active(cls, telegram_id: int, state_active: bool) -> None:
        """
        Обновляет активность профиляпользователя в таблице Profile.

        :param telegram_id: Телеграмм айди пользователя.
        :param state_active: Активен ли профиль у пользователя.
        """

        try:
            async with cls.Session() as request:
                user_profile = await cls.get_user_profile(telegram_id=telegram_id)
                user_profile.active_profile = state_active
                request.add(user_profile)
                await request.commit()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 75] - error updating active profile: [+] {error}")
        
    @classmethod
    async def get_all_id(cls) -> Optional[list]:
        """Возвращает все айдишники пользователей."""

        try:
            async with cls.Session() as request:
                all_profile = await request.execute(select(Users))

                all_id: list = []
                for profile in all_profile.scalars().all():
                    all_id.append(profile.telegram_id)
            return all_id
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 86] - error getting all id: [+] {error}")

    @classmethod
    async def get_statistics(cls) -> Optional[dict]:
        """Возвращает статистику бота."""

        try:
            async with cls.Session() as request:
                all_profile = await request.execute(select(Users))

                statistics: dict = {
                    'count_profile': 0,
                    'count_man': 0,
                    'count_woman': 0,
                    'count_active_profile': 0,
                    'count_unactive_profile': 0,
                    'average_age': 0,
                    'average_age_man': 0,
                    'average_age_woman': 0,
                    'most_common_name': 'None',
                }
                
                list_names: list = []
                for profile in all_profile.scalars().all():
                    statistics['average_age'] += profile.age
                    list_names.append(profile.name.lower().capitalize())
                    statistics['count_profile'] += 1

                    if profile.gender == 'man':
                        statistics['count_man'] += 1
                        statistics['average_age_man'] += profile.age
                    else:
                        statistics['count_woman'] += 1
                        statistics['average_age_woman'] += profile.age

                    if profile.active_profile:
                        statistics['count_active_profile'] += 1

                if statistics['count_profile'] != 0:
                    statistics['average_age'] /= statistics['count_profile']
                if statistics['count_man'] != 0:
                    statistics['average_age_man'] /= statistics['count_man']
                if statistics['count_woman'] != 0:
                    statistics['average_age_woman'] /= statistics['count_woman']

                statistics['most_common_name'] = most_common(list_names)
                statistics['count_unactive_profile'] = statistics['count_profile'] - statistics['count_active_profile']
            return statistics
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - [line: 99] - error getting bot statistics: [+] {error}")
