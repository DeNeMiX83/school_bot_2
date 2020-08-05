from aiogram.dispatcher import FSMContext
from data.config import director_id_list
from funcs import is_director
from keyboards.inline import exit_panel
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from sqlite import cur, con
from states import RegisterClass
from utils.misc import rate_limit


@rate_limit(2)
@dp.message_handler(Text(equals='Создать класс'), is_director)
async def text(msg: Message, state: FSMContext):
    await msg.answer('Введите название\nИли нажмите "Выйти"', reply_markup=exit_panel)
    await RegisterClass.Name.set()


@rate_limit(2)
@dp.message_handler(state=RegisterClass.Name)
async def register(msg: Message, state: FSMContext):
    answer1 = msg.text
    if len(answer1) > 3 and answer1[0].isalpha():
        await msg.answer(text='Не коректные данные'
                              '\nПример: 10, 10Б, 1, 1Б')
        await msg.answer('Введите название\nИли нажмите "Выйти"', reply_markup=exit_panel)
        return
    school = cur.execute('''SELECT school FROM users WHERE user_id = ?''',
                         [msg.from_user.id]).fetchone()[0]
    try:
        cur.execute('''INSERT INTO classes VALUES (NULL, ?, NULL, ?, NULL)''', [answer1, school])
    except Exception as e:
        await msg.answer(text='Такой класс уже существует')
        print(e)
        await state.finish()
        return
    con.commit()
    await msg.answer('Класс добавлен'
                     f'\nНазвание: {answer1}')
    await state.finish()

