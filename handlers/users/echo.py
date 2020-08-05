from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.config import admin_role, director_role, teacher_role, student_role, admin_id_list, \
    director_id_list, teacher_id_list, student_id_list
from keyboards.default import not_role_panel, director_panel, teacher_panel, student_panel, \
    admin_panel
from loader import dp
from sqlite import cur
from utils.misc import rate_limit


@dp.callback_query_handler(text='exit_inline_message', state='*')
async def exit_(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    data = await state.get_data()
    await call.message.delete()
    await state.finish()
    start_panel = data.get('start_panel')
    if start_panel:
        await call.message.answer(text='Хорошо',
                                  reply_markup=start_panel)


@dp.message_handler(text='Выйти', state=[None, '*'])
async def exit(msg: Message, state: FSMContext):
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
        panel = teacher_panel
    elif role == student_role:
        panel = student_panel
    await msg.answer(text='Хорошо', reply_markup=panel)
    await state.finish()


@rate_limit(3)
@dp.message_handler()
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer('Я не знаю что ты пишешь')
