from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from funcs.all_funcs import is_classroom_teacher
from keyboards.inline import register_canteen_boss_buttons
from loader import dp, bot
from sqlite import cur, con


@dp.message_handler(Text(equals=['Главный по столовой']), is_classroom_teacher)
async def canteen_bos(msg: Message):
    print(f'{msg.from_user.full_name} нажал на кнопку: Главный по столовой')
    class_id = cur.execute('''SELECT id FROM classes WHERE bos = ?''',
                           [msg.from_user.id]).fetchone()[0]
    students = cur.execute('''SELECT u.name, s.user
                            FROM students s 
                            LEFT JOIN users u ON s.user = u.user_id WHERE class = ?''',
                           [class_id]).fetchall()
    if not students:
        await msg.answer(text='Учеников нет')
        print(f'{msg.from_user.full_name} нажал на кнопку: Главный по столовой но учеников не было')
        return
    for student, user_id in students:
        await msg.answer(text=f'🧑‍🎓{student}🧑‍🎓',
                         reply_markup=await register_canteen_boss_buttons(user_id))


@dp.callback_query_handler(lambda c: 'register_canteen_boss' in c.data)
async def register_canteen_boss(call: CallbackQuery):
    await call.answer(cache_time=60)
    print(call.data)
    student_id = call.data.split('_')[3]
    user_id = call.from_user.id
    cur.execute('''UPDATE classes set canteen = ? WHERE bos = ?''', [student_id, user_id])
    try:
        await call.message.delete()
    except Exception as e:
        print(f'{call.from_user.full_name} не смог зарегестрировать главного по столовой'
              f'\nОшибка: {e}')
    print(f'{call.from_user.full_name} зарегестрировал главного по столовой в классе с user_id: {student_id} где кл.рук. с user_id: {user_id}')
    await call.message.answer(text='♻️Выполнено♻️')
    await bot.send_message(chat_id=student_id,
                           text='Вы стали главным по столовой👨‍🍳')
    con.commit()