from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import register


async def register_director(school_id):
    panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Добавить директора', callback_data=register.new(
                    what='director',
                    id=f'{school_id}'
                ))
            ]
        ]
    )
    return panel