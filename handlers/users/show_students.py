from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from funcs.all_funcs import correct_user, is_director, check_school_id, classroom_teacher_class_id, is_teacher, \
    is_classroom_teacher
from keyboards.default import show_students_buttons, student_information
from loader import dp, bot
from sqlite import cur, con
from states import ShowClass
from states.show_students_state import ShowStudents


@dp.message_handler(Text(equals='Ученики'), is_classroom_teacher)
async def text(msg: Message, state: FSMContext):
    class_id = await classroom_teacher_class_id(msg)
    students = cur.execute('''SELECT u.name, u.user_name 
                            FROM users u
                            LEFT JOIN students s ON u.user_id = s.user WHERE class = ?''',
                          [class_id]).fetchall()
    print(f'{msg.from_user.full_name} нажал кнопку Ученики')
    await show_students_buttons(msg, students)
    await ShowStudents.Students.set()


@dp.message_handler(is_classroom_teacher, text_contains='Ученик', state=ShowStudents.Students)
async def text(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    student_user_name = msg.text[msg.text.index('@') + 1:]
    student_id = cur.execute('''SELECT user_id FROM users WHERE user_name = ?''', [student_user_name]).fetchone()[0]
    print(f'{msg.from_user.full_name} зашел в ученика user_name: {student_user_name}')
    await student_information(msg, student_user_name)
    await state.update_data(student_id=student_id)