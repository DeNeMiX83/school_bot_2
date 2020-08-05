from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import delete
from sqlite import cur


async def show_school_panel(school_id):
    panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить школу', callback_data=delete.new(
                    what='school',
                    id=f'{school_id}'
                ))
            ]
        ]
    )
    return panel