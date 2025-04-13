from database.bans_db import BansUser

async def check_ban(telegram_id: int) -> bool:
    """
    Проверяет забанен ли пользователь.

    :param telegram_id: Телеграмм айди пользователя.
    """

    profile_db = await BansUser.get_ban_user(telegram_id=telegram_id)
    if profile_db != None and profile_db.status_ban == True:
        return True
    else:
        return False
