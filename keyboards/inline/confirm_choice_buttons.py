from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import confirm_choice


async def confirm_choice_buttons(who):
    panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=confirm_choice.new(
                    who=who,
                    choice='yes'
                )),
                InlineKeyboardButton(text='Нет', callback_data=confirm_choice.new(
                    who=who,
                    choice='no'
                ))
            ]
        ]
    )
    return panel