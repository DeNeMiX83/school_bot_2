from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

student_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Столовая🥣'),
        ]
    ],
    resize_keyboard=True
)