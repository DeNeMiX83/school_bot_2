from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import admin_role, director_role, teacher_role, student_role, classroom_teacher_id_list
from funcs.all_funcs import is_classroom_teacher
from keyboards.default import not_role_panel, director_panel, teacher_panel, student_panel, \
    admin_panel
from loader import dp
from sqlite import cur
from states.show_students_state import ShowStudents
from utils.misc import rate_limit


@dp.message_handler(text='Выйти', state=[None, '*'])
async def exit(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал выйти через кейборд кнопку')
    panel = await get_user_panel(msg)
    await msg.answer(text='Хорошо', reply_markup=panel)
    await state.finish()


@rate_limit(1)
@dp.message_handler(state='*')
async def bot_echo(message: types.Message, state: FSMContext):
    panel = await get_user_panel(message)
    await message.answer('Я не знаю что ты пишешь', reply_markup=panel)
    await state.finish()


@dp.callback_query_handler(state='*')
async def call_echo(call: CallbackQuery):
    await call.message.answer('Я не могу выполнить эту команду')
    await call.message.delete()


async def get_user_panel(msg):
    user_id = msg.from_user.id
    try:
        role = cur.execute('''SELECT role FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]
    except Exception as e:
        print(e)
        await msg.answer(text='Вы не авторизованы'
                              '\n нажмите или напишите /start')
        return
    panel = not_role_panel
    if role == admin_role:
        panel = admin_panel
    elif role == director_role:
        panel = director_panel
    elif role == teacher_role:
        panel = teacher_panel()
        if await is_classroom_teacher(msg):
            panel = teacher_panel(True)
    elif role == student_role:
        panel = student_panel
    return panel
