from database.profile_db import ProfileUser
from typing import Union

async def check_active_profile(telegram_id: int) -> Union[str, bool]:
    """
    Проверяет активен ли профиль пользователя.

    :param telegram_id: Телеграмм айди пользователя.
    """
    
    profile = await ProfileUser.get_user_profile(telegram_id=telegram_id)
    if profile != None and profile.active_profile:
        return 'active'
    elif  profile != None and not profile.active_profile:
        return 'unactive'
    else:
        return False
