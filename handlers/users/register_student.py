from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from data.config import not_role, teacher_role, teacher_id_list, student_id_list, student_role
from funcs.all_funcs import check_school_id, correct_user, is_classroom_teacher
from funcs.delete import student_delete
from keyboards.default import teacher_panel
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur, con
from states import RegisterStudent
from states.show_students_state import ShowStudents


@dp.message_handler(Text(equals='Добавить ученика'), is_classroom_teacher, state='*')
async def text(msg: Message, state: FSMContext):
    print(await state.get_state())
    print(f'{msg.from_user.full_name} нажал кнопку Добавить ученика')
    await msg.answer(text='Напишите имя ученика с @', reply_markup=await exit_panel())
    await RegisterStudent.first()


@dp.message_handler(state=RegisterStudent.name)
async def register(msg: Message, state: FSMContext):
    text = msg.text
    school_id = await check_school_id(msg.from_user.id)
    user = await correct_user(text, msg)
    if not user:
        print(f'{msg.from_user.full_name} не смог зарегестрировать ученика')
        return
    class_id = cur.execute('''SELECT id FROM classes WHERE bos = ?''', [msg.from_user.id]).fetchone()[0]
    try:
        cur.execute('''INSERT INTO students VALUES(NULL, ?, ?, 0)''', [class_id, user])
        cur.execute('''UPDATE users set role = ?, school = ? WHERE user_id = ?''',
                    [student_role, school_id, user])
    except Exception as e:
        await msg.answer(text='Такой ученик уже существует')
        print(f'{msg.from_user.full_name} не смог зарегестрировать ученика'
              f'\nОшибка: {e}')
        await state.finish()
        return
    con.commit()
    student_id_list.append(user)
    print(f'{msg.from_user.full_name} добавил ученика с user_name: {text}')
    await msg.answer('Ученик добавлен', reply_markup=teacher_panel(True))
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна команду: /start')
    await state.finish()


@dp.message_handler(Text(equals='Удалить ученика'), is_classroom_teacher, state=ShowStudents.Students)
async def text(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Удалить ученика')
    data = await state.get_data()
    student_id = data['student_id']
    await student_delete(student_id)
    await state.finish()
    await msg.answer(text='Сделано', reply_markup=teacher_panel(True))

