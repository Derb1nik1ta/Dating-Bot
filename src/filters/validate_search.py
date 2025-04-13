import re


async def validate_message(text: str) -> bool:
    """
    Проверяет корректно ли введено сообщение.

    :param text: Сообщение для пользователя.
    """
    
    return False if text == 'None' or len(text) > 150 or bool(re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", text)) else True


async def validate_input_reason(text: str) -> bool:
    """
    Проверяет корректно ли введена причина жалобы.

    :param text: Причина жалобы.
    """

    return False if text == 'None' or len(text) > 150 else True