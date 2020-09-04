from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    ClassStart = State()
    Write = State()