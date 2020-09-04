from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.exit import exit_panel_button

canteen_notise_ditails_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Подробности', callback_data='canteen_notice_details'),
                exit_panel_button
            ]
        ]
    )
