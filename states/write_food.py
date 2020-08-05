from aiogram.dispatcher.filters.state import StatesGroup, State


class WriteFood(StatesGroup):
    Name = State()
    Price = State()
    Quantity = State()
