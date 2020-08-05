from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import answer

food_write = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✅',
                                 callback_data=answer.new(type='food_write', answer='+')),
            InlineKeyboardButton(text='❌',
                                 callback_data=answer.new(type='food_write', answer='-'))
        ]
    ]
)