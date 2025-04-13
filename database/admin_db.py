from sqlalchemy import select
from .models import Admins
from .Database import DataBase
from src.core.date_now import get_date_now
from src.core.loggers import error_logger
from typing import Optional

class AdminUser(DataBase):
    """Класс для взаимодействия с таблицей Admins."""
    @classmethod
    async def add_admin_user(cls, telegram_id: int) -> Optional[bool]:
        """
        Добавляет нового админа в таблицу Admins.

        :param telegram_id: Телеграмм айди пользователя.
        :return: True, если пользователь внесен в БД,
                False, если пользователь уже есть в БД.
        """
        
        try:
            admin = await cls.get_admin_user(telegram_id=telegram_id)
            if admin == None:
                async with cls.Session() as request:
                    request.add(Admins(telegram_id=telegram_id))
                    await request.commit()
                return True
            else:
                return False
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error adding an admin: [+] {error}")
    
    @classmethod
    async def delete_admin_user(cls, telegram_id: int) -> Optional[bool]:
        """
        Удаляет админа с таблицы Admins.

        :param telegram_id: Телеграмм айди пользователя.
        :return: True, если пользователь удалился с БД,
                False, если пользователя не было в БД.
        """

        try:
            async with cls.Session() as request:
                admin = await cls.get_admin_user(telegram_id=telegram_id)
                if admin != None:
                    await request.delete(admin)
                    await request.commit()
                    return True
                else:
                    return False
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error deletion an admin: [+] {error}")

    @classmethod
    async def get_admin_user(cls, telegram_id: int) -> Optional[Admins]:
        """
        Возвращает данные о админе с таблицы Admins.

        :param telegram_id: Телеграмм айди пользователя.
        :return: Скалярный объект.
        """

        try:
            async with cls.Session() as request:
                result = await request.execute(select(Admins).where(Admins.telegram_id==telegram_id))
                return result.scalar()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting admin: [+] {error}")

    @classmethod
    async def get_admin_users(cls) -> Optional[list]:
        """Возвращает айдишники всех админов с таблицы Admins."""

        try:
            async with cls.Session() as request:
                info = await request.execute(select(Admins))

                result = []
                for el in info.scalars().all():
                    result.append(str(el.telegram_id))
                return result
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting id admins: [+] {error}")

