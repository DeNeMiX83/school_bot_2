from aiogram.dispatcher import FSMContext
from data.config import admin_id_list
from funcs.all_funcs import is_admin
from keyboards.default import show_school_buttons, admin_panel, school_information
from loader import dp
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from sqlite import cur, con
from states import ShowSchool


@dp.message_handler(Text(equals='Школы'), is_admin)
async def text(msg: Message, state: FSMContext):
    print(f'{msg.from_user.full_name} нажал кнопку Школы')
    schools = cur.execute('''select * from schools ''').fetchall()
    await show_school_buttons(msg, schools)


@dp.message_handler(is_admin, text_contains='Школа')
async def text(msg: Message, state: FSMContext):
    text = msg.text
    print(f'{msg.from_user.full_name} зашел в {text} школу')
    shool_id = cur.execute('''SELECT id FROM schools WHERE name = ?''', [text[9:]]).fetchone()[0]
    await school_information(msg)
    await state.update_data(school_id=shool_id,
                            start_panel=admin_panel)
    await ShowSchool.School.set()


@dp.message_handler(text='Удалить школу', state=ShowSchool.School)
async def delete_school(msg: Message, state: FSMContext):
    data = await state.get_data()
    cur.execute('''DELETE FROM schools WHERE id = ?''', [data.get('school_id')])
    await msg.answer(text='Школа удалена',
                     reply_markup=admin_panel)
    con.commit()
    await state.finish()
    await msg.delete()
