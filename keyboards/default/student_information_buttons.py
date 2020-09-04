from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def student_information(msg, name):
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    panel.add(KeyboardButton(text='Удалить ученика'))
    panel.add(KeyboardButton(text='Выйти'))
    await msg.answer(text=f'Ученик: {name}',
                     reply_markup=panel)
