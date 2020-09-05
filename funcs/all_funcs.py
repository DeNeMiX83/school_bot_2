from re import search

import emoji
from aiogram.types import Message

from data.config import admin_id_list, director_id_list, teacher_id_list, student_id_list, \
    classroom_teacher_id_list, not_role
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
    try:
        return cur.execute('''SELECT class FROM students WHERE user = ?''',
                               [msg.from_user.id]).fetchone()[0]
    except Exception as e:
        print('Ошибка при взятии айди класса')
        print(e)
        print(cur.execute('''SELECT class FROM students WHERE user = ?''',
                           [msg.from_user.id]).fetchone())


async def classroom_teacher_class_id(msg):
    try:
        return cur.execute('''SELECT id FROM classes WHERE bos = ?''',
                               [msg.from_user.id]).fetchone()[0]
    except Exception as e:
        print('Ошибка при взятии айди класса')
        print(e)
        print(cur.execute('''SELECT class FROM students WHERE user = ?''',
                           [msg.from_user.id]).fetchone())


async def reset_role(user_id):
    cur.execute('''UPDATE users SET role = ? WHERE user_id = ?''', [not_role, user_id])
    con.commit()


async def chek_correct_classroom_name(msg, class_name):
    if len(class_name) > 3 or class_name[0].isalpha():
        await msg.answer(text='Не коректные данные'
                              '\nПример: 10, 10Б, 1, 1Б')
        await msg.answer('Напишите название\nИли нажмите "Выйти"', reply_markup=await exit_panel())
        print(f'{msg.from_user.full_name} не смог создать класс: некорректные данные')
        return False
    return True


async def correct_user(name, msg):
    if name[0] != '@' or len(name) < 3 or name[1:] == msg.from_user.username:
        await msg.answer(text='Не коректные данные',
                         reply_markup=exit_panel)
        return
    user = cur.execute('''SELECT user_id, role FROM users WHERE user_name = ?''', [name[1:]]).fetchone()
    if not user:
        await msg.answer(text='Такого пользователя нет в системе')
        await msg.answer(text='\nПопросите его зайти в бота и повторите попытку')
        return
    role = user[1]
    if role != not_role:
        await msg.answer(text='Такой пользователь не может быть добавлен'
                              f'\nЕго роль: {role}')
        return
    return user[0]


def give_emoji_free_text(text):
    text = text.encode('utf8')
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text


def get_class_name(text):
    class_name = search(r'\d{2}\w', text)
    if not class_name:
        class_name = search(r'\d{2}', text)
    if not class_name:
        class_name = search(r'\d\w', text)
    if not class_name:
        class_name = search(r'\d', text)
    return class_name[0]


async def check_school_id(user_id):
    return cur.execute('''SELECT school FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]


async def is_admin(message: Message):
    return message.from_user.id in admin_id_list


async def is_director(message: Message):
    return message.from_user.id in director_id_list


async def is_teacher(message: Message):
    return message.from_user.id in teacher_id_list


async def is_classroom_teacher(message: Message):
    return message.from_user.id in classroom_teacher_id_list


async def is_student(message: Message):
    return message.from_user.id in student_id_list