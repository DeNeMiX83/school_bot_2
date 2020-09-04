from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from data.config import admin_id_list, director_role, director_id_list
from funcs.all_funcs import correct_user, is_admin
from keyboards.default import admin_panel
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur, con
from states import ShowSchool
from states.register_director_state import RegisterDirerctor


@dp.message_handler(Text(equals='Добавить директора'), is_admin, state=ShowSchool.School)
async def text(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Добавить директора')
    await msg.answer(text='Напишите имя директора с @', reply_markup=await exit_panel())
    await RegisterDirerctor.first()


@dp.message_handler(state=RegisterDirerctor.name)
async def name(msg: Message, state: FSMContext):
    text = msg.text
    data = await state.get_data()
    user = await correct_user(text, msg)
    if not user:
        print(f'{msg.from_user.full_name} не смог зарегестрировать директора: не корректные данные ')
        return
    try:
        cur.execute('''INSERT INTO directors VALUES (NULL, NULL, ?)''', [user])
    except Exception as e:
        await msg.answer(text='Такой директор уже существует')
        print(f'{msg.from_user.full_name} не смог зарегестрировать пользователя'
              f'\nОшибка: {e}')
        await state.finish()
        return
    cur.execute('''UPDATE users set role = ?, school = ? WHERE user_name = ?''',
                [director_role, data.get('school_id'), text[1:]])
    con.commit()
    director_id_list.append(user)
    print(f'{msg.from_user.full_name} зарегестрировал директора с user_name: {text}')
    await msg.answer('Пользователь добавлен',
                     reply_markup=admin_panel)
    await bot.send_message(chat_id=user, text='Напишите или нажмите \nна  команду: /start')
    await state.finish()