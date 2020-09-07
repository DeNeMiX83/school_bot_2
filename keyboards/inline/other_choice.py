from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import answer


async def other_choice(buttons, data, type_=''):
    panel = InlineKeyboardMarkup(row_width=2)
    panel.add(*(InlineKeyboardButton(text=f'{button}: {data[button]}',
                                     callback_data=answer.new(type=type_, answer=button))
                for button in buttons))
    panel.add(
        InlineKeyboardButton(text='сохранить',
                             callback_data=answer.new(type=type_, answer='save')),
        InlineKeyboardButton(text='Отмена',
                             callback_data='canteen_write_food_exit')
    )
    return panel
