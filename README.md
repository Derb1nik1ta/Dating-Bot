<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>README — Бот знакомств</title>
        <style type="text/css">
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }
            
            h1 {
                text-align: center;
                color: #ffa500;
                margin-bottom: 30px;
            }
            
            p {
                margin-top: 10px;
                margin-bottom: 10px;
            }
            
            ul, ol {
                list-style-position: inside;
                margin-left: 20px;
            }
            
            pre code {
                display: block;
                white-space: pre-wrap;
                word-break: break-all;
                overflow-x: auto;
                border-radius: 5px;
                padding: 10px;
                background-color: #eee;
                max-width: 100%;
            }
            
            a {
                color: #007bff;
                text-decoration: none;
            }
            
            strong {
                font-weight: bold;
            }
            
            em {
                font-style: italic;
            }
        </style>
    </head>
<body>
    <h1 style="color:#0ABAB5;">🩵 Бот знакомств — твой идеальный помощник в поиске второй половинки!</h1>

    <!-- <p><strong>Описание:</strong></p> -->
    <p style="text-align: center;">Наш бот знакомств💖 — идеальное решение для тех, кто ищет искреннюю связь и настоящую любовь. Интерфейс прост и удобен, регистрация✍️ займет лишь несколько минут, а дальнейший поиск партнера начнется автоматически. Важнейшая задача для нас — безопасность🔐 ваших данных и защита от неприятных ситуаций, поэтому мы строго контролируем качество анкет и репутации участников. Найдите свою вторую половину💞 легко и комфортно с нашим умным помощником, подарив себе шанс на счастливую встречу и теплые отношения👩‍❤️‍👨.</p> 
    <hr/>
    
    <p><strong>Особенности проекта:</strong></p>
    <ul>
        <li>Удобное меню навигации</li>
        <li>Возможность подбора идеальных пар</li>
        <li>Персонализированные рекомендации</li>
        <li>Простое управление профилем</li>
        <li>Моментальные уведомления о симпатии</li>
    </ul>
    <hr/>
    
    <p><strong>Требования к среде разработки:</strong></p>
    <ul>
        <li>Python ≥= 3.12</li>
        <li>Redis</li>
        <li>MySQL | Sqlite</li>
        <li>Aiogram 3.x</li>
    </ul>
    <hr/>
    
    <p><strong>Установка и запуск:</strong></p>
    <pre><code>
    git clone https://github.com/Derb1nik1ta/Dating-Bot.git
    cd Dating-Bot
    pip install -r requirements.txt
    # for windows:
    python main.py run
    # for linux:
    python3 main.py run
    </code></pre>
    
    <!-- <p><strong>Тестирование функционала:</strong></p> -->
    <p>Перед запуском бота создайте в корне проекта файл .env и напишите следующие константы:</p>

    <pre><code>
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
    </code></pre>

    <p>Все значения в скобках нужно изменить на свои.</p>
    <hr/>
    
    <p><strong>Лицензия:</strong></p>
    <p>Данный проект распространяется под лицензией MIT License.</p>
    <hr>

    <p>Спасибо, что выбрали наш продукт! Если возникнут вопросы или пожелания, пожалуйста, напишите нам в <a href="https://t.me/dfbffc">телеграмм</a>.</p>
    
    <p><em>Ждем вас среди наших пользователей! 😍❤️</em></p>
</body>
</html>
