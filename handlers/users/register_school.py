from aiogram.dispatcher import FSMContext
from data.config import admin_id_list
from funcs.all_funcs import is_admin
from keyboards.inline import exit_panel
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from sqlite import cur, con
from states import RegisterSchool


@dp.message_handler(Text(equals='Создать школу'), is_admin)
async def text(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Создать школу')
    await msg.answer(text='Напишите название\nИли нажмите "Выйти"',
                     reply_markup=await exit_panel())
    await RegisterSchool.Name.set()


@dp.message_handler(state=RegisterSchool.Name)
async def register(msg: Message, state: FSMContext):
    answer1 = msg.text
    try:
        cur.execute('''INSERT INTO schools VALUES (NULL, ?)''', [answer1])
    except Exception as e:
        await msg.answer(text='Такая школа уже существует')
        print(f'{msg.from_user.full_name} не смог зарегестрировать пользователя: ошибка при сохранении в бд'
              f'\nОшибка: {e}')
        await state.finish()
        return
    con.commit()
    print(f'{msg.from_user.full_name} зарегестрировал школу с именем: {answer1}')
    await msg.answer('Школа добавлена'
                     f'\nНазвание: {answer1}')
    await state.finish()