from database.admin_db import AdminUser

async def check_admin(telegram_id: int) -> bool:
    """
    Проверяет является ли пользователь админом.

    :param telegram_id: Телеграмм айди пользователя.
    """
    
    if await AdminUser.get_admin_user(telegram_id=telegram_id) != None:
        return True
    else:
        return False
