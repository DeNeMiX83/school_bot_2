from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterClass(StatesGroup):
    Name = State()