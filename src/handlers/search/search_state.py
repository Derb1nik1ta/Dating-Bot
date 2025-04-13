from aiogram.fsm.state import StatesGroup, State

class SearchState(StatesGroup):
    """Состояния для просмотра анкет."""
    
    # for continue search
    continue_search = State()
    # for send message
    input_message = State()
    # for continue search profile
    continue_search = State()
    # for view likes
    view_likes = State()
    # for complaint in search 
    input_reason = State()
    # for complain in view likes
    view_likes_input_reason = State()