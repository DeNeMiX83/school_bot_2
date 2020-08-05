from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

director_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать класс'),
            KeyboardButton(text='Добавить учителя')
        ],
        [
            KeyboardButton(text='Классы'),
        ]
    ],
    resize_keyboard=True
)