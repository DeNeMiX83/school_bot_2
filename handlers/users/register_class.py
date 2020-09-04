from aiogram.dispatcher import FSMContext
from data.config import director_id_list
from funcs.all_funcs import is_director
from funcs.delete import classroom_delete
from keyboards.default import director_panel
from keyboards.inline import exit_panel
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from sqlite import cur, con
from states import RegisterClass, ShowClass
from utils.misc import rate_limit


@rate_limit(2)
@dp.message_handler(Text(equals='Создать класс'), is_director)
async def text(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал на кнопку Создать класс')
    await msg.answer('Напишите название\nИли нажмите "Выйти"', reply_markup=await exit_panel())
    await RegisterClass.Name.set()


@rate_limit(2)
@dp.message_handler(state=RegisterClass.Name)
async def register(msg: Message, state: FSMContext):
    answer1 = msg.text
    if len(answer1) > 3 or answer1[0].isalpha():
        await msg.answer(text='Не коректные данные'
                              '\nПример: 10, 10Б, 1, 1Б')
        await msg.answer('Напишите название\nИли нажмите "Выйти"', reply_markup=await exit_panel())
        print(f'{msg.from_user.full_name} не смог создать класс: некорректные данные')
        return
    school = cur.execute('''SELECT school FROM users WHERE user_id = ?''',
                         [msg.from_user.id]).fetchone()[0]
    try:
        cur.execute('''INSERT INTO classes VALUES (NULL, ?, NULL, ?, NULL)''', [answer1, school])
    except Exception as e:
        await msg.answer(text='Такой класс уже существует')
        print(f'{msg.from_user.full_name} не смог создать класс'
              f'\nОшибка: {e}')
        await state.finish()
        return
    print(f'{msg.from_user.full_name} создал класс с названием: {answer1}')
    con.commit()
    await msg.answer('Класс добавлен'
                     f'\nНазвание: {answer1}')
    await state.finish()


@dp.message_handler(Text(equals='Удалить класс'), is_director, state=ShowClass.Class)
async def text(msg: Message, state: FSMContext):
    data = await state.get_data()
    class_name = data['class_name']
    await classroom_delete(class_name)
    await state.finish()
    await msg.answer(text='Класс удален',
                     reply_markup=director_panel)

