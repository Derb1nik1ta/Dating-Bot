from config.config import settings

async def check_owner(telegram_id: int) -> bool:
    """
    Проверяет является ли пользователь владельцем.

    :param telegram_id: Телеграмм айди пользователя.
    """

    if str(telegram_id) == settings.ID_OWNER:
        return True
    else:
        return False
    