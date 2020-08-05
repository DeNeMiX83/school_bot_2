from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.exit import exit_panel_button
from keyboards.inline.callback_datas import confirm_choice
from sqlite import cur


async def canteen_zeroize_buttons(user_id, class_id):
    panel = InlineKeyboardMarkup()
    if cur.execute('''SELECT canteen FROM classes WHERE id = ?''', [class_id]).fetchone()[0] == user_id:
        panel.add(InlineKeyboardButton(text='Обнулить',
                                       callback_data=confirm_choice.new(
                                           who='canteen',
                                           choice='zeroize')),
                  exit_panel_button)
    return panel