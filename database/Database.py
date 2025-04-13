from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from .models import *
from config.config import settings
from src.core.date_now import get_date_now
from src.core.loggers import error_logger


class DataBase():
    """
    Класс для создания и подключения к БД.

    :param __data_db: Данные о базе данных.
    :param __db_name: Имя базы данных.
    :param __db_user: Юзернейм базы данных.
    :param __db_password: Пароль базы данных.
    :param __db_host: Хост базы данных.
    :param __url_connect: Ссылка для подключения к базе данных.
    :param __async_engine: Асинхронный движок.
    :param Session: Сессия для взаимодействия с базой данных.
    """

    # for mysql
    # __data_db: str = settings.get_data_db()
    # __db_name: str = __data_db['DB_NAME']
    # __db_user: str = __data_db['DB_USER']
    # __db_password: str = __data_db['DB_PASSWORD']
    # __db_host: str = __data_db['DB_HOST']
    # __url_connect: str = f'mysql+aiomysql://{__db_user}:{__db_password}@{__db_host}/{__db_name}?charset=utf8mb4'
    
    # for sqlite3
    __url_connect: str = 'sqlite+aiosqlite://tests/database.db'

    __async_engine = create_async_engine(__url_connect)
    Session = async_sessionmaker(bind=__async_engine, class_=AsyncSession)

    @classmethod
    async def create_db(cls) -> None:
        """Создает БД."""
        
        try:
            async with cls.__async_engine.begin() as connect:
                await connect.run_sync(Base.metadata.create_all)
        except Exception as error:
            error_logger.error(f"{await get_date_now()} - {__file__.split('\\')[-1]} - error creating tables: [+] {error}")
