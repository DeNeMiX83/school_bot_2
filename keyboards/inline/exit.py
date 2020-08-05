from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

exit_panel_button = InlineKeyboardButton(text='Выйти', callback_data='exit_inline_message')
exit_panel = InlineKeyboardMarkup().add(exit_panel_button)

