import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from data.config import morph
from funcs.all_funcs import student_class_id, is_student, check_school_id
from keyboards.inline import other_choice, food_write, canteen_zeroize_buttons, \
    confirm_choice_buttons, exit_panel, canteen_notise_panel, canteen_notise_ditails_panel, \
    canteen_quantity_all_panel, exit_from_food_panel
from keyboards.inline.callback_datas import answer, confirm_choice
from sqlite import cur, con
from keyboards.default import canteen_panel
from loader import dp, bot
from states import WriteFood
from utils.misc import rate_limit
import datetime as dt

canteen_data = {}


@rate_limit(3)
@dp.message_handler(Text(equals=['Столовая🥣']), is_student)
async def canteen(msg: Message):
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел в столовую')
    await msg.answer(text='Выбери', reply_markup=canteen_panel)
    await register_class_in_canteen(msg)


@rate_limit(2)
@dp.message_handler(Text(equals=['Записать еду🍱']), is_student)  # кнопка
async def food(msg: Message):
    class_id = await student_class_id(msg)
    food = await take_food(msg, class_id)
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел в что дают')
    day = dt.datetime.now()
    new_day = cur.execute('''SELECT * FROM days
                            WHERE day = ? and month = ? and year = ?''',
                          [day.day, day.month, day.year]).fetchone()
    if new_day:  # если сегодня запись есть то отмечаться заного не надо
        await msg.answer(text='Вы сегодня отмечались')
        return
    if len(food) == 2:
        await msg.answer(text='Данные на сегодня внесены')
        return
    elif food == 'write':
        await msg.answer(text='Данные заполняются другим пользователем')
        return
    canteen_data[class_id]['food'] = 'write'
    await msg.answer('Напишите количество учеников в классе или нажмите все', reply_markup=canteen_quantity_all_panel)
    await WriteFood.Quantity.set()


@dp.callback_query_handler(text='canteen_write_food_exit',
                           state=[WriteFood.Quantity, WriteFood.Name, WriteFood.Price])
async def write_food_exit_func(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} вышел из что дают')
    await call.message.answer(text='Отменена регистрация еды на сегодня')
    await call.message.delete()
    await state.finish()
    await register_class_in_canteen(call)


@dp.callback_query_handler(text='canteen_quantity_all', state=WriteFood.Quantity)
async def canteen_quantity_all_func(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} ввел сколько людей через кнопку все')
    await call.message.delete()
    class_id = await student_class_id(call)
    quantity = len(cur.execute('''SELECT * FROM students WHERE class = ?''', [class_id]).fetchall())
    await write_quantity(call.message, state, quantity)


@dp.message_handler(state=WriteFood.Quantity)  # кол-во учеников
async def price_food(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    class_id = await student_class_id(msg)
    try:
        quantity = int(msg.text)
    except Exception as e:
        print(e)
        await msg.answer(text='Напишите корректные цифры', reply_markup=exit_from_food_panel)
        return
    students_q = len(cur.execute('SELECT user FROM students WHERE class = ?', [class_id]).fetchall())
    if quantity > students_q:
        comment = morph.parse('ученик')[0]
        word = comment.make_agree_with_number(students_q).word
        await msg.answer(text=f'❌Вы не правы в вашем классе {students_q} {word}❌')
        await msg.answer('Напишите количество учеников в классе ',
                         reply_markup=canteen_quantity_all_panel)
        return
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} ввел сколько людей вручную: {quantity}')
    await write_quantity(msg, state, quantity)


@dp.message_handler(state=WriteFood.Name)  # название блюда
async def food_name_func(msg: Message, state: FSMContext):
    name = msg.text
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} ввел название блюда: {name}')
    data = await state.get_data()
    data['Название'] = name
    await state.update_data(data)
    if data.get('name'):
        await save_food(msg, state)
        return
    await state.update_data(name=True)
    await msg.answer(text='Напишите цену блюда', reply_markup=exit_from_food_panel)
    await WriteFood.Price.set()


@dp.message_handler(state=WriteFood.Price)  # цена блюда
async def food_price_func(msg: Message, state: FSMContext):
    price = msg.text
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} ввел цену блюда: {price}')
    try:
        price = float(msg.text)
    except Exception as e:
        await msg.answer(text='Напишите корректные цифры')
        return
    data = await state.get_data()
    data['Цена'] = price
    await state.update_data(data)
    await save_food(msg, state)
    await state.set_state(None)


async def save_food(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(text='Есть что поменять?',
                     reply_markup=await other_choice(['Название', 'Цена', 'Ученики'], data,
                                                     type_='food_name'))


@dp.callback_query_handler(answer.filter(type='food_name'),
                           state=[WriteFood.Quantity, WriteFood.Name, WriteFood.Price, None])  # изменения по блюду
async def different_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    choice = callback_data['answer']
    user_id = call.from_user.id
    await call.message.delete()
    if choice == 'Ученики':
        await call.message.answer('Напишите количество учеников в классе',
                                  reply_markup=canteen_quantity_all_panel)
        await WriteFood.Quantity.set()
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} редактирует учеников')
    elif choice == 'Название':
        await call.message.answer('Напишите название блюда', reply_markup=exit_from_food_panel)
        await WriteFood.Name.set()
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} редактирует название')
    elif choice == 'Цена':
        await call.message.answer('Напишите цену блюда')
        await WriteFood.Price.set()
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} редактирует цену')
    elif choice == 'save':
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} сохранил блюдо')
        class_id = cur.execute('''SELECT class FROM students WHERE user = ?''',
                               [call.from_user.id]).fetchone()[0]
        data = await state.get_data()
        canteen_data[class_id]['food'] = [data.get('Название'), data.get('Цена')]
        canteen_data[class_id]['quantity'] = data.get('Ученики')
        people = cur.execute('''SELECT user FROM students WHERE class = ?''', [class_id]).fetchall()
        people = map(lambda id: id[0], people)
        for user_id in people:
            await bot.send_message(chat_id=user_id,
                                   text='Блюдо добавлено'
                                        '\n------------------------------'
                                        '\nИдите записаться😋')
        await state.finish()


@rate_limit(2)
@dp.message_handler(Text(equals=['Записаться🖋']), is_student)  # кнопка
async def write(msg: Message):
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел записаться')
    class_id = await student_class_id(msg)
    food = await take_food(msg, class_id)
    print('еда в записаться', food)
    print(canteen_data)
    if not food or food == 'write':
        await msg.answer(text='Блюдо не добавлено')
        print(
            f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел записаться, но блюдо не было добавлено'
            f'{canteen_data}')
        return
    await msg.answer(text=f'🥘Блюдо: {food[0]}'
                          f'\n💶Цена: {food[1]}',
                     reply_markup=food_write)
    con.commit()


@dp.callback_query_handler(answer.filter(type='food_write'), state='*')  # запись платно/бесплатно
async def food_write_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    choice = callback_data['answer']
    await call.message.delete()
    user_id = call.from_user.id
    class_id = cur.execute('''SELECT class FROM students WHERE user = ?''',
                           [user_id]).fetchone()[0]
    if choice == '+':
        canteen_data[class_id]['who'][user_id] = choice
    elif choice == '-':
        canteen_data[class_id]['who'][user_id] = choice
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} записался: {choice}')
    await call.message.answer(text='♻️Вы записаны♻️')
    await state.finish()


@rate_limit(2)
@dp.message_handler(Text(equals=['Отметить📝']), is_student)  # кнопка
async def food_note_func(msg: Message):
    class_id = await student_class_id(msg)
    food = await take_food(msg, class_id)
    user_id = msg.from_user.id
    if not food or food == 'write':
        await msg.answer(text='Блюдо не добавлено')
        print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел отметить, но блюдо не было добавлено'
              f'{canteen_data}')
        return
    quantity_now = len(canteen_data[class_id]['who'])
    quantity = canteen_data[class_id]['quantity']
    if quantity != quantity_now:
        await msg.answer(text='Не все отметились'
                              f'\nОсталось: {quantity - quantity_now}',
                         reply_markup=canteen_notise_ditails_panel)
        print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел отметить, но не все отметились')
        return
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел отметить и отметил')
    await canteen_summ(msg, class_id, food)


@dp.callback_query_handler(text='canteen_notice_details')  # подтверждение отмечания
async def canteen_notice_func(call: CallbackQuery, state):
    user_id = call.from_user.id
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} зашел отметить и нажал побробнее')
    await call.message.delete()
    class_id = await student_class_id(call)
    people = []
    for id in await stay_people_id(class_id):
        id = cur.execute('''SELECT name FROM users WHERE user_id = ?''', [id]).fetchone()[0]
        people.append(id)
    await call.message.answer(text='⬇️Вот эти герои⬇️' +
                                   '\n------------------------------\n🔅' +
                                   '\n🔅'.join(people),
                              reply_markup=canteen_notise_panel)


@dp.callback_query_handler(text='canteen_notify_stay_people')  # рассылка тем кто не записался
async def canteen_notify_stay_people_func(call: CallbackQuery, state):
    user_id = call.from_user.id
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} зашел отметить и уведомил остальных записаться')
    await call.message.delete()
    class_id = await student_class_id(call)
    people = await stay_people_id(class_id)
    for id in people:
        await bot.send_message(chat_id=id, text='Вы забыли записаться')


@dp.callback_query_handler(text='canteen_notice')  # подтверждение отмечания
async def canteen_notice_func(call: CallbackQuery, state):
    user_id = call.from_user.id
    print(f'{call.from_user.full_name} роль: ученик, id: {user_id} зашел отметить потои подробнее и нажал отметить')
    await call.message.delete()
    class_id = await student_class_id(call)
    food = await take_food(call, class_id)
    await canteen_summ(call, class_id, food)


@dp.message_handler(Text(equals=['Суммы💰']), is_student)  # кнопка
async def food_sum_func(msg: Message):
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел в суммы')
    class_id = await student_class_id(msg)
    data = cur.execute('''SELECT u.name, s.canteen 
                        FROM students s 
                        LEFT JOIN users u ON s.user = u.user_id WHERE s.class = ?''',
                       [class_id]).fetchall()
    await msg.answer(text='⬇️Суммы⬇️'
                          '\n---------------------------\n🔅' +
                          '\n🔅'.join(f'{name}: {price}' for name, price in data),
                     reply_markup=await canteen_zeroize_buttons(msg.from_user.id, class_id))


@dp.callback_query_handler(confirm_choice.filter(who='canteen'))  # обнуление сумм
async def canteen_zeroize_func(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.delete()
    choice = callback_data.get('choice')
    user_id = call.from_user.id
    if choice == 'zeroize':
        await call.message.answer(text='Подтвердите выбор',
                                  reply_markup=await confirm_choice_buttons('canteen'))
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} нажал обнулить суммы')
    elif choice == 'yes':
        cur.execute('''UPDATE students SET canteen = 0''')
        con.commit()
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} нажал обнулить суммы: подтвердил выбор')
        await call.message.answer(text='♻️Операция проведена♻️')
    elif choice == 'no':
        await call.message.answer(text='❌Операция отменена❌')
        print(f'{call.from_user.full_name} роль: ученик, id: {user_id} нажал обнулить суммы: отменил выбор')


async def stay_people_id(class_id):
    people = canteen_data[class_id]['who']
    all_people = cur.execute('''SELECT u.user_id
                                    FROM users u 
                                    LEFT JOIN students s ON u.user_id = s.user WHERE class = ?''',
                             [class_id]).fetchall()
    return map(lambda x: str(x[0]), filter(lambda x: x[0] not in people, all_people))


async def write_quantity(msg, state, quantity):
    data = await state.get_data()
    data['Ученики'] = int(quantity)
    await state.update_data(data)
    if data.get('quantity'):
        await save_food(msg, state)
        return
    await state.update_data(quantity=True)
    await msg.answer(text='Напишите название блюда', reply_markup=exit_from_food_panel)
    await WriteFood.Name.set()


def get_date():
    day = dt.datetime.now()
    return day.day, day.month, day.year


async def write_date_in_db(food, class_id):
    food, price = food
    try:
        cur.execute('''INSERT INTO days VALUES(NULL, ?, ?, ?, ?, ?, ?)''',
                    [class_id, *get_date(), food, price])
    except Exception as e:
        print(f'Ошибка при записи данных в таблицу с днями')
        print(e)


async def write_choice_in_db(people_id, choice):
    day = cur.execute('''SELECT id FROM days WHERE day = ? and month = ? and year = ?''',
                      [*get_date()]).fetchone()[0]
    try:
        cur.execute('''INSERT INTO canteen_journal VALUES (NULL, ?, ?, ?)''',
                    [people_id, day, choice])
    except Exception as e:
        print(f'Ошибка при записи данных в журнал столовой')
        print(e)


async def canteen_summ(msg, class_id, food):
    paid = 0
    free = 0
    price = food[1]
    await write_date_in_db(food, class_id)
    for people_id, choice in canteen_data[class_id]['who'].items():
        if choice == '+':
            cur.execute('''UPDATE students SET canteen = canteen + ? WHERE user = ?''',
                        [price, people_id])
            paid += 1
        elif choice == '-':
            free += 1
        await write_choice_in_db(people_id, choice)
    class_id = await student_class_id(msg)
    for id in await stay_people_id(class_id):
        await write_choice_in_db(id, '-')
    con.commit()
    if isinstance(msg, CallbackQuery):
        msg = msg.message
    await msg.answer(text='⬇️Получилось⬇️'
                          '\n-----------------------------'
                          f'\n💵Платно: {paid}'
                          f'\n💸Бесплатно: {free}')
    try:
        del canteen_data[class_id]
        print('блюдо удалено')
    except KeyError:
        pass


async def take_food(msg, class_id):
    try:
        food = canteen_data[class_id]['food']
        return food
    except Exception as e:
        await register_class_in_canteen(msg)
        food = await take_food(msg, class_id)
        return food


async def register_class_in_canteen(msg):
    class_id = await student_class_id(msg)
    if class_id not in canteen_data:
        canteen_data[class_id] = {'food': [], 'who': {}, 'quantity': 0}

