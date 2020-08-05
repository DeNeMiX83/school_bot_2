from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def register_canteen_boss_buttons(user_id):
    panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Назначить', callback_data=f'register_canteen_boss_{user_id}')
            ]
        ]
    )
    return panel