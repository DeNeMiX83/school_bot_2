from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from funcs.all_funcs import correct_user, is_director, check_school_id, get_class_name
from keyboards.default import show_classes_buttons, director_panel, class_information
from loader import dp, bot
from sqlite import cur, con
from states import ShowClass


@dp.message_handler(Text(equals='Классы'), is_director)
async def text(msg: Message, state: FSMContext):
    school_id = await check_school_id(msg.from_user.id)
    classes = cur.execute('''SELECT * FROM classes WHERE school = ?''',
                          [school_id]).fetchall()
    print(f'{msg.from_user.full_name} директор из школы id: {school_id} нажал кнопку классы')
    await show_classes_buttons(msg, classes)


@dp.message_handler(is_director, text_contains='Класс')
async def text(msg: Message, state: FSMContext):
    text = msg.text
    user_id = msg.from_user.id
    class_name = get_class_name(text)
    school_id = cur.execute('''SELECT school FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]
    print(f'{msg.from_user.full_name} зашел в {class_name} класс')
    await state.update_data(school_id=school_id,
                            start_panel=director_panel,
                            class_name=class_name)
    await class_information(msg, school_id, class_name)
    await ShowClass.Class.set()

