from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

month_of_year_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Январь'),
            KeyboardButton(text='Февраль'),
            KeyboardButton(text='Март')
        ],
        [
            KeyboardButton(text='Апрель'),
            KeyboardButton(text='Май'),
            KeyboardButton(text='Июнь')
        ],
[
            KeyboardButton(text='Июль'),
            KeyboardButton(text='Август'),
            KeyboardButton(text='Сентябрь')
        ],
[
            KeyboardButton(text='Октябрь'),
            KeyboardButton(text='Ноябрь'),
            KeyboardButton(text='Декабрь')
        ],
        [
            KeyboardButton(text='Выйти')
        ]
    ],
    resize_keyboard=True
)