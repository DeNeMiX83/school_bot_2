from aiogram.utils.callback_data import CallbackData

answer = CallbackData('answer', 'type', 'answer')
register = CallbackData('register', 'what', 'id')
delete = CallbackData('delete', 'what', 'id')
confirm_choice = CallbackData('confirm', 'who', 'choice')
exit_from_inline = CallbackData('exit_inline_message', 'where')