from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    Start = State()
    Write = State()