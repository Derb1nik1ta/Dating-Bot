import re


async def validate_gender(gender: str) -> bool:
    """
    Проверяет корректно ли введен пол.

    :param gender: Пол пользователя.
    """
    return True if gender in ('Мужской ♂', 'Женский ♀') else False


async def validate_name(name: str) -> bool:
    """
    Проверяет корректно ли введено имя.

    :param name: Имя пользователя.
    """
    
    return False if name == 'None' else bool(re.fullmatch(r'\w{,12}[а-яА-Яa-zA-Z]', rf'{name}'))


async def validate_age(age: str) -> bool:
    """
    Проверяет корректно ли введен возраст.

    :param age: Возраст пользователя.
    """

    return False if age == 'None' else bool(re.fullmatch(r'[1-9][0-9]', rf'{age}'))


async def validate_city(city: str) -> bool:
    """
    Проверяет корректно ли введен город.

    :param city: Город пользователя.
    """

    return False if city == 'None' else bool(re.fullmatch(r'\w{,15}[а-яА-Яa-zA-Z]', rf'{city}'))


async def validate_description(text: str) -> bool:
    """
    Проверяет корректно ли введено описание.

    :param text: Описание пользователя.
    """

    return False if text == 'None' or len(text) > 150 or bool(re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", text)) else True
