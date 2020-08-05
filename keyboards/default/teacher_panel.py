from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

teacher_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пусто'),
            KeyboardButton(text='Добавить ученика')
        ],
        [
            KeyboardButton(text='Главный по столовой'),
        ]
    ],
    resize_keyboard=True
)