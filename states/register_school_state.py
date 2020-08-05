from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterSchool(StatesGroup):
    Name = State()