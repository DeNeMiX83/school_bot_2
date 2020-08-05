from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

canteen_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Что дают'),
            KeyboardButton(text='Записаться')
        ],
        [
            KeyboardButton(text='Отметить'),
            KeyboardButton(text='Суммы')
        ],
        [
            KeyboardButton(text='Выйти')
        ]
    ],
    resize_keyboard=True
)