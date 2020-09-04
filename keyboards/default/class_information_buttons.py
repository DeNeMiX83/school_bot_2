from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlite import cur


async def class_information(msg, school_id, class_name):
    bos = cur.execute('''SELECT u.name
                    FROM classes c
                    LEFT JOIN users u ON c.bos = u.user_id WHERE c.school = ? and c.name = ?''',
                      [school_id, class_name]).fetchone()[0]
    bos = 'Нету' if bos is None else bos
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text='Добавить кл. рук.')
    if bos != 'Нету':
        button = KeyboardButton(text='Убрать кл. рук.')
    panel.add(button,
              KeyboardButton(text='Удалить класс'))
    panel.add(KeyboardButton(text='Выйти'), KeyboardButton(text='Рассылка'))
    await msg.answer(text='Классный руководитль: '
                          f'\n{bos}',
                     reply_markup=panel)