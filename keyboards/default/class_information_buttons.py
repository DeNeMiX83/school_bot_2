from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlite import cur


async def class_information(msg, school_id):
    bos = cur.execute('''SELECT u.name
                    FROM classes c
                    LEFT JOIN users u ON c.bos = u.user_id WHERE c.school = ?''',
                      [school_id]).fetchone()[0]
    bos = 'Нету' if bos is None else bos
    panel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Добавить кл. рук.'),
                KeyboardButton(text='Удалить класс'),
            ],
            [
                KeyboardButton(text='Выйти')
            ]
        ],
        resize_keyboard=True
    )
    await msg.answer(text='Классный руководитль: '
                          f'\n{bos}',
                     reply_markup=panel)