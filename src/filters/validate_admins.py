import re


async def validate_input_id(telegram_id: str) -> bool:
    """
    Проверяет корректно ли введен айди.

    :param telegram_id: Телеграмм айди.
    """
    
    return False if telegram_id == 'None' else bool(re.fullmatch(r'\d{1,20}', f'{telegram_id}'))


async def validate_input_reason(text: str) -> bool:
    """
    Проверяет длину причины бана.

    :param text: Текст причины бана.
    """

    return False if text == 'None' or len(text) > 150 else True


async def validate_input_text(text: str) -> bool:
    """
    Проверяет длину сообщения.

    :param text: Текст сообщения.
    """

    return False if text == 'None' or len(text) > 350 else True
