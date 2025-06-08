from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    name = State()
    info = State()
    photo = State()