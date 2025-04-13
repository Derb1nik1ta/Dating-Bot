from datetime import datetime
import pytz

async def get_date_now() -> str:
    """Возвращает текущее время."""
    
    return datetime.now(tz=pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")
