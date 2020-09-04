from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message
from data.config import teacher_role, classroom_teacher_id_list
from funcs.all_funcs import check_school_id
from keyboards.default import class_information
from keyboards.inline import made_bos_in_class
from keyboards.inline.callback_datas import register
from loader import bot, dp
from sqlite import cur, con
from states import ShowClass
from utils.misc import rate_limit


async def register_taecher_in_class(msg: Message, teachers):
    if not teachers:
        print(f'{msg.from_user.full_name} не смог добавить кл.рук.: учителей нет')
        await msg.answer(text='Учителей нет')
    for user_id, name in teachers:
        await msg.answer(text=f'Учитель: {name}', reply_markup=await made_bos_in_class(user_id))


@dp.message_handler(Text(equals='Добавить кл. рук.'), state=ShowClass.Class)
async def register_teacher(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Добавить кл.рук.')
    user_id = msg.from_user.id
    school_id = await check_school_id(user_id)
    teachers = cur.execute('''Select user_id, name from users where role = ? and school = ?''',
                           [teacher_role, school_id]).fetchall()
    await register_taecher_in_class(msg, teachers)


@dp.callback_query_handler(register.filter(what='teacher_in_class'), state=ShowClass.Class)
async def register_teacher_in_class_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    class_name = data['class_name']
    teacher_id = int(callback_data.get('id'))
    teacher = cur.execute('''SELECT name FROM classes WHERE bos = ?''', [teacher_id]).fetchone()
    if teacher:
        print(f'{call.from_user.full_name} не смог добавить кл.рук.: Этот учитель является кл.рук. в {teacher[0]} классе')
        await call.message.delete()
        await call.message.answer(text=f'Этот учитель является кл.рук. в {teacher[0]} классе')
        return
    director_id = call.from_user.id
    school_id = await check_school_id(director_id)
    cur.execute('''UPDATE classes set bos = ? WHERE school = ? and name = ?''', [teacher_id, school_id, class_name])
    con.commit()
    await call.message.delete()
    print(f'{call.from_user.full_name} добавил кл.рук с user_name: {teacher_id} в {class_name} класс')
    await class_information(call.message, school_id, class_name)
    await call.message.answer(text='♻️Кл.рук. добавлен♻️')
    await bot.send_message(chat_id=teacher_id, text='Напишите или нажмите \nна  команду: /start')
    classroom_teacher_id_list.append(teacher_id)


@rate_limit(2)
@dp.message_handler(Text(equals='Убрать кл. рук.'), state=ShowClass.Class)
async def delete_teacher_in_class(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    class_name = data['class_name']
    school_id = await check_school_id(user_id)
    user = cur.execute('''SELECT bos FROM classes WHERE name = ? and school = ?''',
                           [class_name, school_id]).fetchone()[0]
    cur.execute('''UPDATE classes SET bos = NULL WHERE name = ? and school = ?''',
                           [class_name, school_id])
    print(f'{msg.from_user.full_name} убрал кл.рук. из {class_name} класса')
    con.commit()
    await msg.answer(text='♻️Кл.рук. убран♻️')
    await class_information(msg, school_id, class_name)
    del classroom_teacher_id_list[classroom_teacher_id_list.index(user)]
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна  команду: /start')



