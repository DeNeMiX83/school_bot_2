from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def show_students_buttons(msg, students):
    panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(*(KeyboardButton(text=f'Ученик: {name}'
                                    f'\nИмя: @{id}') for name, id in students))
    panel.add(KeyboardButton(text='Добавить ученика'), KeyboardButton(text='Выйти'))
    await msg.answer(text='Выберите ученика',
                     reply_markup=panel)