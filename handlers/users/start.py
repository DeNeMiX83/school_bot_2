from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import not_role, admin_role, director_role, teacher_role, student_role
from funcs import *
from keyboards.default import admin_panel, not_role_panel, director_panel, teacher_panel, \
    student_panel
from loader import dp
from sqlite import cur
from utils.misc import rate_limit
 

@rate_limit(2)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    name = message.from_user.full_name
    cur.execute('''SELECT user_id FROM users WHERE user_id = ?''', [user_id])
    if not cur.fetchone():
        if not message.from_user.username:
            await message.answer(text='Укажите в настройках имя пользователя')
            await message.answer(text='Затем отправьте в чат командку /start')
            return
        print(1)
        await register_user(user_id, user_name, name, not_role)
    role = cur.execute('''SELECT role FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]
    panel = not_role_panel
    if role == admin_role:
        panel = admin_panel
    elif role == director_role:
        panel = director_panel
    elif role == teacher_role:
        panel = teacher_panel
    elif role == student_role:
        panel = student_panel
    await message.answer(f'Привет, {name}'
                         f'\nВаша роль: {role}',
                         reply_markup=panel)
