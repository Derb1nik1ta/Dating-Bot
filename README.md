![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)  ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)  ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

# 🩵 Бот знакомств — твой идеальный помощник в поиске второй половинки!

Наш **бот знакомств💖** — идеальное решение для тех, кто ищет __искреннюю связь и настоящую любовь__. Интерфейс прост и удобен, **регистрация✍️** займет лишь __несколько минут__, а дальнейший поиск партнера начнется автоматически. Важнейшая задача для нас — **безопасность**🔐 ваших данных и защита от неприятных ситуаций, поэтому мы __строго контролируем качество анкет__ и репутации участников. Найдите свою вторую половину💞 легко и комфортно с нашим умным помощником, подарив себе шанс на счастливую встречу и **теплые отношения**👫.


## Особенности проекта
- 📖 Удобное меню навигации
- 👩‍❤️‍👨 Возможность подбора идеальных пар
- 🔍 Персонализированные рекомендации
- 🕹️ Простое управление профилем
- 🔔 Моментальные уведомления о симпатии


## Требования к среде разработки
- Python >= 3.12
- Redis
- MySQL
- Aiogram 3.x


## Установка и запуск
```bash
git clone https://github.com/Derb1nik1ta/Dating-Bot.git
cd Dating-Bot
pip install -r requirements.txt
# for windows:
python main.py run
# for linux:
python3 main.py run
```

**Перед запуском бота создайте в корне проекта файл .env и напишите следующие константы:**
```bash
BOT_TOKEN = 'Ваш токен Бота'
ID_OWNER = 'Ваш айди в телеграмм'
ID_GROUP_COMPLAINT = 'Айди группы, куда будут приходить жалобы'
LINK_GROUP_HELP = 'Ссылка на группу с поддержкой'

DB_NAME = 'Имя базы данных'
DB_USER = 'Юзернейм базы данных'
DB_PASSWORD = 'Пароль базы данных'
DB_HOST = 'Хост базы данных'

REDIS_PASSWORD = 'Пароль Редис'
REDIS_HOST = 'Хост Редис'
REDIS_USER = 'Юзернейм Редис'
REDIS_PORT = 'Порт Редис'
REDIS_DB = '0'
```
Все значения в скобках, кроме `REDIS_DB`, нужно изменить на свои.

Если хотите использовать бота без **Редис**, раскомментируйте в файле `main.py` строку `storage = RedisStorage.from_url(url=settings.get_url_redis())` и закомментируйте строку `storage = None`.

## Лицензия
**Данный проект распространяется под лицензией MIT License.**

---

Спасибо, что выбрали наш продукт! Если возникнут ошибки во время работы бота, вопросы или пожелания, пожалуйста, напишите нам в [телеграмм](https://t.me/dfbffc).
