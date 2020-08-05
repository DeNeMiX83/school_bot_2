from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать школу'),
            KeyboardButton(text='Школы'),
        ],
    ],
    resize_keyboard=True
)