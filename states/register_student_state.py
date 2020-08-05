from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStudent(StatesGroup):
    name = State()