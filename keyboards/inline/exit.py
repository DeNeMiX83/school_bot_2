from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import exit_from_inline


async def exit_panel(where='all'):
    panel = None
    if where == 'all':
        panel = exit_panel_button
    else:
        panel = await exit_panel_button_func(where)
    exit_panel = InlineKeyboardMarkup().add(panel)
    return exit_panel


async def exit_panel_button_func(where='all'):
    exit_panel_button = InlineKeyboardButton(text='Отмена', callback_data=exit_from_inline.new(
        where=where))
    return exit_panel_button


exit_panel_button = InlineKeyboardButton(text='Отмена', callback_data=exit_from_inline.new(
        where='all'))

