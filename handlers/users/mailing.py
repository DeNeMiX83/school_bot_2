from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from funcs.all_funcs import is_teacher, check_school_id, classroom_teacher_class_id, is_director
from keyboards.default import show_classes_buttons
from keyboards.inline import exit_panel
from loader import dp, bot
from sqlite import cur
from states import Mailing, ShowClass
from utils.misc import rate_limit


@rate_limit(2)
@dp.message_handler(is_teacher, text='Рассылка')
async def mailing_func(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Рассылка')
    school_id = await check_school_id(msg.from_user.id)
    classes = cur.execute('''SELECT * FROM classes WHERE school = ?''',
                          [school_id]).fetchall()
    await show_classes_buttons(msg, classes)
    await state.update_data(who='учителя')
    await Mailing.ClassStart.set()


@rate_limit(2)
@dp.message_handler(is_director, text='Рассылка', state=ShowClass.Class)
async def mailing_func(msg: Message, state:FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Рассылка')
    school_id = await check_school_id(msg.from_user.id)
    classes = cur.execute('''SELECT * FROM classes WHERE school = ?''',
                          [school_id]).fetchall()
    await show_classes_buttons(msg, classes)
    await state.update_data(who='директора')
    await Mailing.ClassStart.set()


@dp.message_handler(text_contains='Класс', state=Mailing.ClassStart)
async def mailing_classroom(msg: Message, state: FSMContext):
    await msg.answer('\n⬇️Напишите текст в поле ниже⬇️', reply_markup=await exit_panel(where='mailing'))
    await Mailing.Write.set()


@dp.message_handler(state=Mailing.Write)
async def text(msg: Message, state: FSMContext):
    text = msg.text
    user_id = msg.from_user.id
    data = await state.get_data()
    who = data['who']
    await students_mailing(msg, user_id, text, who)
    await msg.answer(text='♻️Сообщение отправлено♻️')
    await state.finish()


async def all_mailing(msg, test):
    pass


async def students_mailing(msg, user_id, text, who):
    class_id = await classroom_teacher_class_id(msg)
    teacher_name = cur.execute('''SELECT u.name 
                                    FROM users u
                                    LEFT JOIN teachers t ON t.user = u.user_id WHERE u.user_id = ?''',
                               [user_id]).fetchone()[0]
    students_id = cur.execute('''SELECT user FROM students WHERE class = ?''', [class_id]).fetchall()
    for id in students_id:
        await bot.send_message(chat_id=id[0], text=f'Сообщение от {who}: {teacher_name}'
                                                   f'\n➡️{text}')