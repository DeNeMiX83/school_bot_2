from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def school_information(msg):
    panel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Пусто'),
                KeyboardButton(text='Добавить директора')
            ],
            [
                KeyboardButton(text='Удалить школу'),
                KeyboardButton(text='Выйти')
            ]
        ],
        resize_keyboard=True
    )
    await msg.answer(text='Выбирайте',
                     reply_markup=panel)