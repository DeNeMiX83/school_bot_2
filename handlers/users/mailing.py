from re import search

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from funcs.all_funcs import is_teacher, check_school_id, classroom_teacher_class_id, get_class_name
from keyboards.default import show_classes_buttons
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur
from states import Mailing
from utils.misc import rate_limit


@rate_limit(2)
@dp.message_handler(text='Рассылка')
async def mailing_func(msg: Message):
    print(f'{msg.from_user.full_name} нажал кнопку Рассылка')
    school_id = await check_school_id(msg.from_user.id)
    classes = cur.execute('''SELECT * FROM classes WHERE school = ?''',
                          [school_id]).fetchall()
    await show_classes_buttons(msg, classes)
    await Mailing.Start.set()


@dp.message_handler(is_teacher, text_contains='Класс', state=Mailing.Start)
async def mailing_classroom(msg: Message, state: FSMContext):
    text = msg.text
    class_name = get_class_name(text)
    print(f'{msg.from_user.full_name} учитель выбрал класс для рассылки: {class_name}')
    await state.update_data(class_name=class_name)
    await msg.answer(f'Класс: {class_name}'
                     '\n⬇️Напишите тест в поле ниже⬇️', reply_markup=await exit_panel('mailing'))
    await Mailing.Write.set()


@dp.message_handler(state=Mailing.Write)
async def text(msg: Message, state: FSMContext):
    text = msg.text
    data = await state.get_data()
    class_name = data['class_name']
    print(f'{msg.from_user.full_name} учитель выбрал класс для рассылки с текстом: {text}')
    user_id = msg.from_user.id
    class_id = cur.execute('SELECT id FROM classes WHERE name = ?',
                           [class_name]).fetchone()[0]
    teacher_name = cur.execute('''SELECT u.name 
                                FROM users u
                                LEFT JOIN teachers t ON t.user = u.user_id WHERE u.user_id = ?''',
                               [user_id]).fetchone()[0]
    students_id = cur.execute('''SELECT user FROM students WHERE class = ?''', [class_id]).fetchall()
    for id in students_id:
        await bot.send_message(chat_id=id[0], text=f'Сообщение от учителя: {teacher_name}'
                                                   f'\n➡️{text}')
    await msg.answer(text='♻️Сообщение отправлено♻️')
    await Mailing.Start.set()
