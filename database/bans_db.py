from sqlalchemy import select
from .models import Bans
from .Database import DataBase
from src.core.date_now import get_date_now
from src.core.loggers import error_logger
from typing import Optional

class BansUser(DataBase):
    """Класс для взаимодействия с таблицей Bans."""
    @classmethod
    async def add_ban_user(cls, telegram_id: int, admin_id: int, reason: Optional[str]='без причины') -> None:
        """
        Вносит пользователя в таблицу Bans.

        :param telegram_id: Телеграмм айди пользователя.
        :param admin_id: Телеграмм айди админа, который выдал бан.
        :param reason: Причина бана.
        """

        try:
            async with cls.Session() as request:
                ban_user = await cls.get_ban_user(telegram_id=telegram_id)

                date_ban: str = await get_date_now()
                if ban_user != None and ban_user.status_ban == False:
                    ban_user.date_ban = date_ban
                    ban_user.admin_id = admin_id
                    ban_user.reason = reason
                    ban_user.count_bans += 1
                    ban_user.status_ban = True

                    request.add(ban_user)
                else:
                    request.add(Bans(
                        telegram_id=telegram_id,
                        admin_id=admin_id,
                        date_ban = date_ban,
                        reason=reason,
                        count_bans=1,
                        status_ban=True))
                await request.commit()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error adding to ban: [+] {error}")

    @classmethod
    async def delete_ban_user(cls, telegram_id: int) -> Optional[bool]:
        """
        Удаляет пользователя с таблицы Bans.

        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                ban_user = await cls.get_ban_user(telegram_id=telegram_id)
                if ban_user == None or not ban_user.status_ban:
                    return False
                else:
                    ban_user.status_ban = False
                    
                    request.add(ban_user)
                    await request.commit()
                    return True
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error deletion ban: [+] {error}")

    @classmethod
    async def get_ban_user(cls, telegram_id: int) -> Optional[Bans]:
        """
        Возвращает информацию о банах пользователя с таблицы Bans.

        :param telegram_id: Телеграмм айди пользователя.
        """

        try:
            async with cls.Session() as request:
                result = await request.execute(select(Bans).where(Bans.telegram_id==telegram_id))
            return result.scalar()
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting ban: [+] {error}")
    
    @classmethod
    async def get_ban_users(cls) -> Optional[str]:
        """Возвращает информацию о банах всех пользователей с таблицы Bans"""
        
        try:
            async with cls.Session() as request:
                ban_users = await request.execute(select(Bans).where(Bans.status_ban==True))
                
                list_bans: list = ban_users.scalars().all()
                if len(list_bans) != 0:
                    result: str = ''
                    for el in list_bans:
                        result += f'Admin ID: {el.admin_id}\n User ID: {el.telegram_id} | кол-во банов: {el.count_bans}, \n{el.date_ban} - причина: {el.reason}\n\n'
                else:
                    result = 'Банов нету🔒'
            return result
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error getting id bans: [+] {error}")
