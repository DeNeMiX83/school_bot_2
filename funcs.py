from aiogram.types import Message

from data.config import admin_id_list, director_id_list, teacher_id_list, student_id_list
from keyboards.inline import exit_panel
from loader import dp
from sqlite import con, cur


async def register_user(user_id, user_name, name, role):
    cur = con.cursor()
    try:
        cur.execute(f'''INSERT INTO users
                    VALUES ({user_id}, '{user_name}', '{name}','{role}', NULL)''')
        print(f'Зарегестрировался: {name}'
              f'\nРоль: {role}')
        con.commit()
    except Exception as e:
        print('Ошибка при регистрации'
              f'\nОшибка: {e}')


async def student_class_id(msg):
    return cur.execute('''SELECT class FROM students WHERE user = ?''',
                           [msg.from_user.id]).fetchone()[0]


async def correct_name(name, msg: Message):
    if name[0] == '@' and len(name) > 3 and name[1:] != msg.from_user.username:
        return True
    await msg.answer(text='Не коректные данные'
                          '\nВведите имя  с @', reply_markup=exit_panel)


async def correct_user_id(name, msg):
    user = cur.execute('''SELECT user_id FROM users WHERE user_name = ?''', [name[1:]]).fetchone()
    if user:
        return user[0]
    await msg.answer(text='Такого пользователя нет в системе')
    await msg.answer(text='\nПопросите его зайти в бота и повторите попытку')


async def check_school_id(user_id):
    return cur.execute('''SELECT school FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]


async def is_admin(message: Message):
    return message.from_user.id in admin_id_list


async def is_director(message: Message):
    return message.from_user.id in director_id_list


async def is_teacher(message: Message):
    return message.from_user.id in teacher_id_list


async def is_student(message: Message):
    return message.from_user.id in student_id_list