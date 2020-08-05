from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from data.config import director_id_list, teacher_role, teacher_id_list
from funcs import correct_name, correct_user_id
from keyboards.inline import exit_panel, made_bos_in_class
from keyboards.inline.callback_datas import register
from loader import dp, bot
from sqlite import cur, con
from states import RegisterTeacher, ShowClass
from funcs import *


async def register_taecher_in_class(msg: Message, teachers):
    if not teachers:
        await msg.answer(text='Учителей нет')
    for user_id, name in teachers:
        await msg.answer(text=f'Учитель: {name}', reply_markup=await made_bos_in_class(user_id))


@dp.message_handler(Text(equals='Добавить кл. рук.'), is_director, state=ShowClass.Class)
async def register_teacher(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    school_id = await check_school_id(user_id)
    teachers = cur.execute('''Select user_id, name from users where role = ? and school = ?''',
                           [teacher_role, school_id]).fetchall()
    await register_taecher_in_class(msg, teachers)


@dp.callback_query_handler(register.filter(what='teacher_in_class'), state=ShowClass.Class)
async def register_teacher_in_class_func(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    teacher_id = callback_data.get('id')
    director_id = call.from_user.id
    school_id = await check_school_id(director_id)
    cur.execute('''UPDATE classes set bos = ? WHERE school = ?''', [teacher_id, school_id])
    con.commit()
    await call.message.delete()
    await call.message.answer(text='♻️Кл.рук. добавлен♻️')




