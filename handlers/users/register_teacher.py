from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from data.config import director_id_list, teacher_role, teacher_id_list
from funcs import correct_name, correct_user_id, is_director
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur, con
from states import RegisterTeacher


async def register_teacher(text, msg, state):
    if not await correct_name(text, msg):
        return
    school_id = cur.execute('''SELECT school FROM users WHERE user_id = ?''',
                            [msg.from_user.id]).fetchone()[0]
    user = await correct_user_id(text, msg)

    if not user:
        await state.finish()
        return
    try:
        cur.execute('''INSERT INTO teachers VALUES(NULL, ?)''', [user])
        cur.execute('''UPDATE users set role = ?, school = ? WHERE user_id = ?''',
                    [teacher_role, school_id, user])
    except Exception as e:
        await msg.answer(text='Такой учитель уже существует')
        print(e)
        await state.finish()
        return
    con.commit()
    teacher_id_list.append(user)
    await msg.answer('♻️Учитель добавлен♻️')
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна  команду: /start')
    await state.finish()


@dp.message_handler(Text(equals='Добавить учителя'), is_director)
async def register(msg: Message, state: FSMContext):
    await msg.answer(text='Введите имя учителя с @', reply_markup=exit_panel)
    await RegisterTeacher.first()


@dp.message_handler(state=RegisterTeacher.name)
async def register(msg: Message, state: FSMContext):
    text = msg.text
    await register_teacher(text, msg, state)