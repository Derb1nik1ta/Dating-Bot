import os
from dotenv import load_dotenv

class Settings():
    """Класс для получения конфигурационных данных."""
    def __init__(self) -> None:
        """
        Создает все необходимые атрибуты для объекта settings.
        
        :param __BOT_TOKEN: Токен для подключения к боту.
        :param ID_OWNER: Айди владельца бота.
        :param USER_OWNER: Юзернейм владельца бота.
        :param ID_GROUP_COMPLAINT: Айди закрытой группы для жалоб.
        :param LINK_GROUP_HELP: Ссылка на группу помощи.
        :param NON_ERASABLE_REDIS_DATA: Кортеж с ключами для хранилища.

        :param __DB_NAME: Имя базы данных.
        :param __DB_USER: Юзернейм базы данных.
        :param __DB_PASSWORD: Пароль базы данных.
        :param __DB_HOST: Хост базы данных.

        :param __REDIS_HOST: Хост Редиса.
        :param __REDIS_PASSWORD: Пароль Редиса.
        :param __REDIS_USER: Юзернейм Редиса.
        :param __REDIS_PORT: Порт Редиса.
        :param __REDIS_DB: Порядок базы данных Редиса.
        """
        
        load_dotenv()
        self.__BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.ID_OWNER = os.getenv('ID_OWNER')
        self.USER_OWNER = os.getenv('USER_OWNER')
        self.ID_GROUP_COMPLAINT = os.getenv('ID_GROUP_COMPLAINT')
        self.LINK_GROUP_HELP = os.getenv('LINK_GROUP_HELP')
        self.NON_ERASABLE_REDIS_DATA = ('id_viewing_profile', 'list_id_profiles', 'adm_id_viewing_profile', 
                                        'adm_list_id_profiles', 'count_like', 'first_like_time')
        self.__DB_NAME = os.getenv('DB_NAME')
        self.__DB_USER = os.getenv('DB_USER')
        self.__DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.__DB_HOST = os.getenv('DB_HOST')
        self.__REDIS_HOST = os.getenv('REDIS_HOST')
        self.__REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        self.__REDIS_USER = os.getenv('REDIS_USER')
        self.__REDIS_PORT = os.getenv('REDIS_PORT')
        self.__REDIS_DB = os.getenv('REDIS_DB')
        
    def get_bot_token(self) -> str:
        """Возвращает токен бота."""

        return self.__BOT_TOKEN
    
    def get_data_db(self) -> dict:
        """Возвращает словарь с данными базы данных."""

        data_db: dict = {
            'DB_NAME': self.__DB_NAME,
            'DB_USER': self.__DB_USER,
            'DB_PASSWORD': self.__DB_PASSWORD,
            'DB_HOST': self.__DB_HOST,
        }
        return data_db

    def get_url_redis(self) -> str:
        """Возваращает ссылку для подключения к Редис."""

        url: str = f'redis://{self.__REDIS_USER}:{self.__REDIS_PASSWORD}@{self.__REDIS_HOST}:{self.__REDIS_PORT}/{self.__REDIS_DB}'
        return url

settings = Settings()
