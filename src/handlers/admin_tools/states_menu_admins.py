from aiogram.fsm.state import StatesGroup, State

class AdminsState(StatesGroup):
    """Состояния для меню модераторов."""

    # menu admins
    menu_admins_state = State()

    # input id for delete ban
    inp_id_delete_ban_state = State()

    # input id for search profile
    inp_id_search_profile_state = State()

    # input id for get ban
    inp_id_get_ban_state = State()
    # input reason for ban
    inp_reason_get_ban_state = State()

    # input id for send message
    inp_id_send_message_state = State()
    # input text for send message
    inp_text_send_message_state = State()

class AdminsSearchState(StatesGroup):
    """Состояния для модерирования анкет."""

    # continue search
    continue_search = State()
    # input reason ban
    inp_reason_ban = State()
    # input text for send message
    inp_text_send_message = State()

class OwnersState(StatesGroup):
    """Состояния для меню владельцев."""

    # menu owners
    menu_owners_state = State()
    # input id for getting admin
    inp_id_get_admin_state = State()
    # input id for deleting admin
    inp_id_delete_admin_state = State()
    # input text for send everyone message
    inp_text_for_send_everyone_state = State()

