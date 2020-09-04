from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

canteen_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Записать еду🍱'),
            KeyboardButton(text='Записаться🖋')
        ],
        [
            KeyboardButton(text='Отметить📝'),
            KeyboardButton(text='Суммы💰')
        ],
        [
            KeyboardButton(text='Таблицы📅')
        ],
        [
            KeyboardButton(text='Выйти')
        ]
    ],
    resize_keyboard=True
)