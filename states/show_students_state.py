from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowStudents(StatesGroup):
    Students = State()
    Student = State