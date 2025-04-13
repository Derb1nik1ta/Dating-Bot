from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для создания моделек."""
    pass


class Users(Base):
    """
    Создает модельку таблицы Profile.

    :param __tablename__: Название таблицы.
    :param id: Айди записи в таблице.
    :param telegram_id: Телеграмм айди пользователя.
    :param user_name: Юзернейм пользователя в телеграмм.
    :param gender: Пол пользователя.
    :param name: Имя пользователя.
    :param age: Возраст пользователя.
    :param city: Город пользователя.
    :param description: Описание пользователя.
    :param media: json-объект со списком айдишников фотографий.
    :param active_profile: Активен ли профиль у пользователя.
    """
    
    __tablename__ = 'Profile'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_name: Mapped[str] = mapped_column(String(32), nullable=False)

    gender: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(12))
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(Text(150))
    media: Mapped[str] = mapped_column(Text)
    active_profile: Mapped[bool] = mapped_column(Boolean, default=True)


class Like(Base):
    """
    Создает модельку таблицы Like.

    :param __tablename__: Название таблицы.
    :param id: Айди записи в таблице.
    :param telegram_id: Телеграмм айди пользователя.
    :param like: json-объект со списком айдишников пользователей, которые лайкнули профиль.
    :param message: json-объект со списком айдишников пользователей, которые лайкнули профиль.
    """

    __tablename__ = 'Like'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey('Profile.telegram_id'))

    like: Mapped[str] = mapped_column(Text, default='[]')
    message: Mapped[str] = mapped_column(Text, default='[]')


class Admins(Base):
    """
    Создает модельку таблицы Admins.

    :param __tablename__: Название таблицы.
    :param id: Айди записи в таблице.
    :param telegram_id: Телеграмм айди пользователя.
    """

    __tablename__ = 'Admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey('Profile.telegram_id'))


class Bans(Base):
    """
    Создает модельку таблицы Bans.

    :param __tablename__: Название таблицы.
    :param id: Айди записи в таблице.
    :param telegram_id: Телеграмм айди пользователя.
    :param admin_id: Телеграм айди админа.
    :param date_ban: Дата бана.
    :param reason: Причина бана. 
    :param count_bans: Количество банов за все время.
    :param status_ban: Забанен ли пользователь сейчас.
    """

    __tablename__ = 'Bans'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, ForeignKey('Profile.telegram_id'))
    admin_id: Mapped[int] = mapped_column(Integer)
    date_ban: Mapped[str] = mapped_column(String(50))
    reason: Mapped[str] = mapped_column(Text)
    count_bans: Mapped[int] = mapped_column(Integer, default=0)
    status_ban: Mapped[bool] = mapped_column(Boolean)
