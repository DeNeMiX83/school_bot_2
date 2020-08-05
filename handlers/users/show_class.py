from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from data.config import director_id_list
from funcs import correct_name, correct_user_id, is_director
from keyboards.default import show_classes_buttons, director_panel, class_information
from keyboards.inline import exit_panel
from keyboards.inline.callback_datas import register
from loader import dp, bot
from sqlite import cur, con
from states import ShowClass


@dp.message_handler(Text(equals='Классы'), is_director)
async def text(msg: Message, state: FSMContext):
    classes = cur.execute('''SELECT * FROM classes''').fetchall()
    await show_classes_buttons(msg, classes)


@dp.message_handler(is_director, text_contains='Класс')
async def text(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    school_id = cur.execute('''SELECT school FROM users WHERE user_id = ?''', [user_id]).fetchone()[0]
    await class_information(msg, school_id)
    await state.update_data(school_id=school_id,
                            start_panel=director_panel)
    await ShowClass.Class.set()

