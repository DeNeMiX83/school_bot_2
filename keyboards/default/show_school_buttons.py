from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message


async def show_school_buttons(msg: Message, schools):
    if not schools:
        await msg.answer(text='❌Школ нету❌')
        return
    panel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(*(KeyboardButton(text=f'🔰Школа: 🏫{school[1]}') for school in schools))
    panel.add(KeyboardButton(text='Выйти'))
    await msg.answer(text='Выберите школу',
                     reply_markup=panel)