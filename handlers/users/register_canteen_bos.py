from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from funcs import is_teacher
from keyboards.inline import register_canteen_boss_buttons
from loader import dp, bot
from sqlite import cur, con


@dp.message_handler(Text(equals=['Главный по столовой']), is_teacher)
async def canteen_bos(msg: Message):
    class_id = cur.execute('''SELECT id FROM classes WHERE bos = ?''',
                           [msg.from_user.id]).fetchone()[0]
    students = cur.execute('''SELECT u.name, s.user
                            FROM students s 
                            LEFT JOIN users u ON s.user = u.user_id WHERE class = ?''',
                           [class_id]).fetchall()
    if not students:
        await msg.answer(text='Учеников нет')
        return
    for student, user_id in students:
        await msg.answer(text=f'🧑‍🎓{student}🧑‍🎓',
                         reply_markup=await register_canteen_boss_buttons(user_id))


@dp.callback_query_handler(lambda c: 'register_canteen_boss' in c.data)
async def register_canteen_boss(call: CallbackQuery):
    await call.answer(cache_time=60)
    user_id = call.data.split('_')[3]
    cur.execute('''UPDATE classes set canteen = ? WHERE bos = ?''', [user_id, call.from_user.id])
    try:
        await call.message.delete()
    except Exception as e:
        print(e)
    await call.message.answer(text='Выполнено')
    await bot.send_message(chat_id=user_id,
                           text='Вы стали главным по столовой')
    con.commit()