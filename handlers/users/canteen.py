from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from funcs import student_class_id, is_student
from keyboards.inline import other_choice, food_write, canteen_zeroize_buttons, \
    confirm_choice_buttons, exit_panel, canteen_notise_panel
from keyboards.inline.callback_datas import answer, confirm_choice
from sqlite import cur, con
from keyboards.default import canteen_panel, student_panel
from loader import dp, bot
from states import WriteFood
from utils.misc import rate_limit


canteen_data = {}


async def canteen_summ(msg, class_id, food):
    paid = 0
    free = 0
    price = food[1]
    for people_id, choice in canteen_data[class_id]['who'].items():
        print(people_id, choice)
        if choice == '+':
            cur.execute('''UPDATE students SET canteen = canteen + ? WHERE user = ?''',
                        [price, people_id])
            paid += 1
        elif choice == '-':
            free += 1
    con.commit()
    await msg.answer(text='⬇️Получилось⬇️'
                          '\n-----------------------------'
                          f'\n💰Платно: {paid}'
                          f'\n💸Бесплатно: {free}')
    del canteen_data[class_id]


@rate_limit(6)
@dp.message_handler(Text(equals=['Столовая']), is_student)
async def canteen(msg: Message):
    await msg.answer(text='Выбери', reply_markup=canteen_panel)
    class_id = await student_class_id(msg)
    if class_id not in canteen_data:
        canteen_data[class_id] = {'food': False, 'who': {}, 'quantity': 0}


@rate_limit(2)
@dp.message_handler(Text(equals=['Что дают']), is_student)  # кнопка
async def food(msg: Message):
    class_id = await student_class_id(msg)
    try:
        food = canteen_data[class_id]['food']
    except Exception as e:
        await msg.answer(text='Ошибка',
                         reply_markup=student_panel)
        return
    if not food:
        await msg.answer('Введите количество учеников в классе', reply_markup=exit_panel)
        await WriteFood.Quantity.set()
    else:
        await msg.answer('Данные заполнены')


@dp.message_handler(state=WriteFood.Quantity)  # кол-во учеников
async def price_food(msg: Message, state: FSMContext):
    quantity = msg.text
    if not quantity.isdigit():
        await msg.answer(text='Введите корректные цифры')
        return
    data = await state.get_data()
    data['Ученики'] = int(quantity)
    await state.update_data(data)
    if data.get('quantity'):
        await save_food(msg, state)
        return
    await state.update_data(quantity=True)
    await msg.answer(text='Введите название блюда')
    await WriteFood.Name.set()


@dp.message_handler(state=WriteFood.Name)  # название блюда
async def food_name_func(msg: Message, state: FSMContext):
    name = msg.text
    data = await state.get_data()
    data['Название'] = name
    await state.update_data(data)
    if data.get('name'):
        await save_food(msg, state)
        return
    await state.update_data(name=True)
    await msg.answer(text='Введите цену блюда')
    await WriteFood.Price.set()


@dp.message_handler(state=WriteFood.Price)  # цена блюда
async def food_price_func(msg: Message, state: FSMContext):
    price = msg.text
    if not price.isdigit():
        await msg.answer(text='Введите корректные цифры')
        return
    data = await state.get_data()
    data['Цена'] = int(price)
    await state.update_data(data)
    await save_food(msg, state)


async def save_food(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(text='Есть что поменять?', reply_markup=await other_choice(['Название', 'Цена', 'Ученики'], data, type_='food_name'))


@dp.callback_query_handler(answer.filter(type='food_name'), state='*')  # изменения по блюду
async def different_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    choice = callback_data['answer']
    await call.message.delete()
    if choice == 'Ученики':
        await call.message.answer('Введите количество учеников в классе')
        await WriteFood.Quantity.set()
    elif choice == 'Название':
        await call.message.answer('Введите название блюда')
        await WriteFood.Name.set()
    elif choice == 'Цена':
        await call.message.answer('Введите цену блюда')
        await WriteFood.Price.set()
    elif choice == 'save':
        class_id = cur.execute('''SELECT class FROM students WHERE user = ?''',
                               [call.from_user.id]).fetchone()[0]
        data = await state.get_data()
        canteen_data[class_id]['food'] = [data.get('Название'), data.get('Цена')]
        canteen_data[class_id]['quantity'] = data.get('Ученики')
        for user_id in canteen_data[class_id]['who']:
            await bot.send_message(chat_id=user_id,
                                   text='Блюдо добавлено'
                                        '\n------------------------------'
                                        '\nИдите отмечаться😋')
        await state.finish()


@rate_limit(2)
@dp.message_handler(Text(equals=['Записаться']), is_student)  # кнопка
async def write(msg: Message):
    class_id = await student_class_id(msg)
    try:
        food = canteen_data[class_id]['food']
    except Exception as e:
        await msg.answer(text='Ошибка',
                         reply_markup=student_panel)
        return
    if not food:
        await msg.answer(text='Блюдо не добавлено')
        return
    await msg.answer(text=f'Блюдо: {food[0]}'
                          f'\nЦена: {food[1]}',
                     reply_markup=food_write)
    con.commit()


@dp.callback_query_handler(answer.filter(type='food_write'), state='*')  # запись платно/бесплатно
async def food_write_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    choice = callback_data['answer']
    await call.message.delete()
    user = call.from_user.id
    class_id = cur.execute('''SELECT class FROM students WHERE user = ?''',
                           [user]).fetchone()[0]
    if choice == '+':
        canteen_data[class_id]['who'][user] = choice
    elif choice == '-':
        canteen_data[class_id]['who'][user] = choice
    await call.message.answer(text='♻️Вы записаны♻️')
    await state.finish()


@rate_limit(5)
@dp.message_handler(Text(equals=['Отметить']), is_student)  # кнопка
async def food_note_func(msg: Message):
    class_id = await student_class_id(msg)
    try:
        food = canteen_data[class_id]['food']
    except Exception as e:
        await msg.answer(text='Ошибка',
                         reply_markup=student_panel)
        return
    if not food:
        await msg.answer(text='Блюдо не добавлено')
        return
    quantity_now = len(canteen_data[class_id]['who'])
    quantity = canteen_data[class_id]['quantity']
    if quantity != quantity_now:
        await msg.answer(text='Не все отметились'
                              f'\nОсталось: {quantity - quantity_now}',
                         reply_markup=canteen_notise_panel)
        return
    await canteen_summ(msg, class_id, food)


@dp.callback_query_handler(text='canteen_notice')  # подтверждение отмечания
async def canteen_notice_func(call: CallbackQuery, state):
    await call.message.delete()
    class_id = await student_class_id(call)
    food = canteen_data[class_id]['food']
    await canteen_summ(call.message, class_id, food)


@dp.message_handler(Text(equals=['Суммы']), is_student)  # кнопка
async def food_sum_func(msg: Message):
    class_id = await student_class_id(msg)
    data = cur.execute('''SELECT u.name, s.canteen 
                        FROM students s 
                        LEFT JOIN users u ON s.user = u.user_id WHERE s.class = ?''', [class_id]).fetchall()
    await msg.answer(text='⬇️Суммы⬇️'
                          '\n---------------------------\n🔅' +
                          '\n🔅'.join(f'{name}: {price}' for name, price in data),
                     reply_markup=await canteen_zeroize_buttons(msg.from_user.id, class_id))


@dp.callback_query_handler(confirm_choice.filter(who='canteen'))  # обнуление сумм
async def canteen_zeroize_func(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.delete()
    choice = callback_data.get('choice')
    if choice == 'zeroize':
        await call.message.answer(text='Подтвердите выбор',
                                  reply_markup=await confirm_choice_buttons('canteen'))
    elif choice == 'yes':
        cur.execute('''UPDATE students SET canteen = 0''')
        con.commit()
        await call.message.answer(text='♻️Операция проведена♻️')
    elif choice == 'no':
        await call.message.answer(text='❌Операция отменена❌')