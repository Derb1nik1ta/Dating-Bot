from datetime import timedelta, datetime

async def check_like_limit(data: dict) -> dict:
    """
    Проверяет превысил ли пользователь лимит лайков.

    :param data: Данные пользователя с Редис.
    """

    if 'count_like' in data:
        count_like = data['count_like']
    else:
        count_like = 0
        data['first_like_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    delta = timedelta(minutes=1)
    first_like_time = datetime.strptime(data['first_like_time'], '%Y-%m-%d %H:%M:%S') + delta
    last_like_time = datetime.now()
    
    if count_like >= 50 and first_like_time < last_like_time:
        data['count_like'] = 1
        data['first_like_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return data
    elif count_like < 50:
        data['count_like'] = count_like + 1
        return data
    else:
        return False
