import csv

from xlsxwriter import Workbook
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from data.config import student_role
from funcs.all_funcs import is_student, student_class_id, give_emoji_free_text
from keyboards.default import month_of_year_panel
from keyboards.inline import help_for_table_button, url_google_table_button
from loader import dp, bot
from sqlite import cur

MONTH = ['Январь', 'Февраль', 'Март',
         'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь',
         'Октябрь', 'Ноябрь', 'Декабрь']


async def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


async def xls_writer(data, path, month):
    workbook = Workbook(path)
    worksheet = workbook.add_worksheet(month)
    for row, line in enumerate(data):
        for col, item in enumerate(line):
            worksheet.write(row, col, item)
    workbook.close()


async def get_data_for_table(msg, month, school_id, class_id):
    days = cur.execute('''SELECT day FROM days WHERE month = ? and class = ?''',
                       [month, class_id]).fetchall()
    users = cur.execute('''SELECT user_id, name FROM users WHERE school = ? and role = ?''',
                        [school_id, student_role]).fetchall()
    foods = await get_food(month, class_id)
    data = list()
    data.append(['День'])
    for day in days:
        data.append([day[0]])
    for user_id, name in users:
        #name = give_emoji_free_text(name)
        data[0].append(name)
        choices = await get_choice(month, user_id)
        for i, day in enumerate(days):
            data[i + 1].append(choices.get(day[0], '-'))
    data[0].append('Еда')
    data[0].append('Цена')
    for i, info in enumerate(foods):
        food, price = info
        data[i + 1].append(food)
        data[i + 1].append(price)
    return data


async def get_choice(month, user_id):
    info = cur.execute(
        '''SELECT d.day, c.choice 
        FROM days d LEFT JOIN canteen_journal c 
        ON d.id = c.day WHERE d.month = ? and c.user = ?''',
        [month, user_id]).fetchall()
    info = {day: choice for day, choice in info}
    return info


async def get_food(month, class_id):
    info = cur.execute(
        '''SELECT food, price
        FROM days WHERE month = ? and class = ?''',
        [month, class_id]).fetchall()
    return info


@dp.message_handler(Text(equals=['Таблицы📅']), is_student)  # кнопка
async def table_func(msg: Message):
    await msg.answer(text='Выбери',
                     reply_markup=month_of_year_panel)
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} зашел в таблицы')


@dp.message_handler(Text(equals=MONTH), is_student)  # кнопка
async def create_table_func(msg: Message):
    text = msg.text
    month = MONTH.index(text) + 1
    user_id = msg.from_user.id
    print(f'{msg.from_user.full_name} роль: ученик, id: {user_id} выбрал создать таблицу на: {MONTH[month - 1]}')
    user_id = msg.from_user.id
    school_id = cur.execute('''SELECT school FROM users WHERE user_id = ?''', [user_id]).fetchone()[
        0]
    class_id = await student_class_id(msg)
    data = await get_data_for_table(msg, month, school_id, class_id)
    if len(data) == 1:
        await msg.answer(text='Нет информации за этот месяц')
        return
    await msg.answer(text='Хорошо')
    path = f'canteen/{MONTH[month - 1]}({school_id}_{class_id}).xlsx'
    await xls_writer(data, path, MONTH[month - 1])
    with open(path, 'rb') as file:
        await bot.send_document(chat_id=msg.from_user.id,
                                document=file,
                                reply_markup=help_for_table_button)


@dp.callback_query_handler(is_student, text='help_for_table')
async def helf_for_table_func(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(text='Если у вас не правильно открывается таблица '
                                   'и колонки в ней спутаны, предлагаю открыть этот файл в '
                                   'google таблицах через компьютер',
                              reply_markup=url_google_table_button)
