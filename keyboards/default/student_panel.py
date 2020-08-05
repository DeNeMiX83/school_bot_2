from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

student_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пусто'),
            KeyboardButton(text='Пусто')
        ],
        [
            KeyboardButton(text='Столовая'),
        ]
    ],
    resize_keyboard=True
)