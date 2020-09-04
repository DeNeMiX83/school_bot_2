from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

canteen_quantity_all_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Все', callback_data='canteen_quantity_all'),
                InlineKeyboardButton(text='Выйти', callback_data='canteen_write_food_exit')
            ]
        ]
    )