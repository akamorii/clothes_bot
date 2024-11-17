from aiogram.fsm.state import StatesGroup, State

class Make_order(StatesGroup):
    collection = State()
    color = State()
    size = State()
    