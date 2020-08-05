from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import register


async def made_bos_in_class(user_id):
    panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Назначить', callback_data=register.new(
                    what='teacher_in_class',
                    id=f'{user_id}',
                ))
            ]
        ]
    )
    return panel