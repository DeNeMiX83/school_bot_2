from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from data.config import admin_id_list, director_role, director_id_list
from funcs import correct_name, correct_user_id, is_admin
from keyboards.default import admin_panel
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur, con
from states import ShowSchool
from states.register_director_state import RegisterDirerctor


@dp.message_handler(Text(equals='Добавить директора'), is_admin, state=ShowSchool.School)
async def text(msg: Message, state: FSMContext):
    await msg.answer(text='Введите имя директора с @', reply_markup=exit_panel)
    await RegisterDirerctor.first()


@dp.message_handler(state=RegisterDirerctor.name)
async def name(msg: Message, state: FSMContext):
    text = msg.text
    data = await state.get_data()
    if not await correct_name(text, msg):
        return
    user = await correct_user_id(text, msg)
    if not user:
        return
    try:
        cur.execute('''INSERT INTO directors VALUES (NULL, NULL, ?)''', [user])
    except Exception as e:
        await msg.answer(text='Такой директор уже существует')
        print(e)
        await state.finish()
        return
    cur.execute('''UPDATE users set role = ?, school = ? WHERE user_name = ?''',
                [director_role, data.get('school_id'), text[1:]])
    con.commit()
    director_id_list.append(user)
    await msg.answer('Пользователь добавлен',
                     reply_markup=admin_panel)
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна  команду: /start')
    await state.finish()