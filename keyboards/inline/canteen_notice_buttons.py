from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.exit import exit_panel_button

canteen_notise_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отметить', callback_data='canteen_notice'),
                exit_panel_button
            ]
        ]
    )
