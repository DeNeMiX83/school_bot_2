from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

not_role_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пусто')
        ]
    ],
    resize_keyboard=True
)