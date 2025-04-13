from config.config import settings

""" Start """
start_message = 'Этот бот🤖 поможет тебе найти🔍'\
                'новые знакомства или отношения❤️\n\n'\
                'Выберите действие👇'


""" Menu """
menu_message = 'Выберите действие👇'

""" Help """
# !
help_message = f'<a href="{settings.LINK_GROUP_HELP}">Чат поддержки🧰</a>'


""" Search """
start_search_message = '💫🔍'

input_text_message = 'Введите сообщение для пользователя💬'

mutual_like_message = 'У вас взаминая симпатия👩‍❤️‍👨\nНачинайте общаться🥳'

completing_likes_message = 'Лайки закончились💫\nСмотреть анкеты 👉 /search'

input_reason_complaint_message = 'Введите причину жалобы:'

complain_successful_delivered_message = 'Жалоба отправлена✅'

""" Validate Search """
validate_like_message = 'Твой лимит лайков закончился😓\nВозращайся через час⏳'

validate_view_likes_message = 'У вас пока нету лайков😕'

validate_input_message = 'Сообщение не должно содержать ссылок🔗 и больше 150 символов🔤'

validate_search_message = 'Нету подоходящих анкет😕'

validate_input_reason_complaint_message = ' '

""" Edit Profile """
input_gender_message = 'Выберите пол🧍‍♂️|🧍‍♀️'

input_name_message = 'Введите имя👇'

input_age_message = 'Возраст🔞'

input_city_message = 'Город🏙'

input_description_message = 'Описание📝'

input_media_message = 'Отправьте %s из 3 фотографий📷'

finish_input_message = 'Профиль успешно записан❤️\n'\
                       'Для просмотра анкет 👉 /search'

profile_unactive_message = 'Профиль отключен🟥'
profile_active_message = 'Профиль включен🟩'


""" Validate Edit Profile """
validate_gender_message = 'Такого пола не существует☠️'

validate_name_message = 'Имя должно содержать только русские🇷🇺 и английские буквы🏴󠁧󠁢󠁥󠁮󠁧󠁿 и не длиннее 12 символов🔤'

validate_age_message = 'Возраст может быть от 10 до 99📅'

validate_city_message = 'Название города может содержать только русские🇷🇺 и английские буквы🏴󠁧󠁢󠁥󠁮󠁧󠁿 и не длиннее 15 символов🔤'

validate_description_message = 'Описание не должно содержать ссылок🔗 и больше 150 символов🔤'

validate_media_message = 'Это не фото🖼'

validate_record_message = 'Произошла ошибка записи😕'

validate_reg_message = 'Ты еще не зарегистрирован👤\n'\
                               'для заполнения анкеты 👉 /reg'

validate_active_message = 'Для просмотра анкет📋 \nнужно включить профиль🗣'

""" For Admins """
menu_admins_message = 'Инструменты модератора:'

input_reason_message = 'Введите причину:'

input_text_message = 'Введите сообщение для пользователя:'

unban_message = 'Вы были разбанены⭐\nСоблюдайте правила⚠️'

# !
ban_message = 'Вы находитесь в бане🔒\n'\
             f'Оспорить бан: <a href="{settings.LINK_GROUP_HELP}">Чат поддержки🧰</a>'

get_ban_message = 'Пользователь успешно забанен✅'

delete_ban_message = 'Пользователь успешно разблокирован✅'

message_successful_delivered_message = 'Сообщение успешно доставлено✅'

search_admins_message = '👮🔍'


""" Validate For Admins """
validate_admin_message = 'У вас недостаточно прав🔗'

validate_input_reason_message = 'Причина не может быть длинее 150 символов⚠️'

validate_get_ban_message = 'Пользователь уже находится в бане❌'

validate_delete_ban_message = 'Пользователь не находится в бане❌'

validate_input_text_message = 'Сообщение должно содержать не более 350 символов⚠️'

validate_search_profile_message = 'Пользователя нету в бд❌'

validate_input_id_send_message = 'Неправильный формат🆔 или пользователя нету в бд❌'

validate_ban_admin_message = 'Вы не можете банить админов❌'

validate_send_message = 'Ошибка отправки уведомления⚠️'


""" For Owners """
menu_owners_message = 'Инструменты владельца:'

input_id_message = 'Введите айди🆔'

input_text_send_everyone_message = 'Введите для всех пользователей сообщение:'

message_successful_delivered_messages = 'Сообщения успешно доставлены✅'

get_admin_message = 'Админка была успешно выдана✅'

delete_admin_message = 'Админка была успешно убрана✅'


""" Validate For Owners """
validate_input_id_message = 'Неправильный формат🆔'

validate_get_admin_message = 'У этого пользователя уже есть админка❌'

validate_delete_admin_message = 'Пользователь не является админом❌'


