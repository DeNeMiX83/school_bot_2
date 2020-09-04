from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

url_google_table_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ссылка на google таблицы',
                                 url='https://docs.google.com/spreadsheets/u/0/')
        ]
    ]
)