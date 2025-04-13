from database.profile_db import ProfileUser

async def check_id(telegram_id: int) -> bool:
    """
    Проверяет есть ли пользователь в БД в таблице Profile.

    :param telegram_id: Телеграмм айди пользователя.
    """
    
    if await ProfileUser.get_user_profile(telegram_id=telegram_id) != None:
        return True
    else:
        return False
