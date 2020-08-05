from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def show_classes_buttons(msg, classes):
    if not classes:
        await msg.answer(text='❌Классов нету❌')
        return
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    panel.add(*(KeyboardButton(text=f'🛎Класс {class_[1]}🛎') for class_ in classes))
    panel.add(KeyboardButton(text='Выйти'))
    await msg.answer(text='Выберите класс',
                     reply_markup=panel)