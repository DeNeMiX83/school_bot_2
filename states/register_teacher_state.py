from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterTeacher(StatesGroup):
    name = State()