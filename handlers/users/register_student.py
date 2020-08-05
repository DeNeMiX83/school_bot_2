from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from data.config import not_role, teacher_role, teacher_id_list, student_id_list, student_role
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur, con
from states import RegisterStudent
from funcs import correct_name, correct_user_id, is_teacher, check_school_id


@dp.message_handler(Text(equals='Добавить ученика'), is_teacher)
async def text(msg: Message):
    user_id = msg.from_user.id
    if user_id not in teacher_id_list:
        return
    await msg.answer(text='Введите имя ученика с @', reply_markup=exit_panel)
    await RegisterStudent.first()


@dp.message_handler(state=RegisterStudent.name)
async def register(msg: Message, state: FSMContext):
    text = msg.text
    school_id = await check_school_id(msg.from_user.id)
    if not await correct_name(text, msg):
        return
    user = await correct_user_id(text, msg)
    if not user:
        await state.finish()
        return
    class_id = cur.execute('''SELECT id FROM classes WHERE bos = ?''', [msg.from_user.id]).fetchone()[0]
    try:
        cur.execute('''INSERT INTO students VALUES(NULL, ?, ?, 0)''', [class_id, user])
        cur.execute('''UPDATE users set role = ?, school = ? WHERE user_id = ?''',
                    [student_role, school_id, user])
    except Exception as e:
        await msg.answer(text='Такой ученик уже существует')
        print(e)
        await state.finish()
        return
    con.commit()
    student_id_list.append(user)
    await msg.answer('Ученик добавлен')
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна команду: /start')
    await state.finish()
