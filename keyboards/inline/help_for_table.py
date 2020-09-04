from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

help_for_table_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Помощь',
                                 callback_data='help_for_table')
        ]
    ]
)