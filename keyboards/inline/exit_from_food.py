from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

exit_from_food_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отмена', callback_data='canteen_write_food_exit')
            ]
        ]
    )