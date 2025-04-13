from aiogram.fsm.state import StatesGroup, State

class MenuState(StatesGroup):
    """Состояние для меню."""
    
    menu = State()
