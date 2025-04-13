from aiogram.fsm.state import StatesGroup, State

class EditProfileState(StatesGroup):
    """Состояния во время изменения профиля."""

    input_gender_state = State()

    input_name_state = State()

    input_age_state = State()

    input_city_state = State()

    input_description_state = State()

    input_media_state_1 = State()
    input_media_state_2 = State()
    input_media_state_3 = State()