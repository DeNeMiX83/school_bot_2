import os

import pymorphy2
from dotenv import load_dotenv

from sqlite import cur

load_dotenv()
admin_role = 'Админ🤖'
director_role = 'Директор🧮'
teacher_role = 'Учитель📚'
student_role = 'Ученик🎒'
not_role = 'Нету❌'

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
]

admin_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                                 [admin_role])]
director_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                                    [director_role])]
classroom_teacher_id_list = [user[0] for user in cur.execute('''SELECT bos FROM classes''')]

teacher_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                                   [teacher_role])]
student_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                                   [student_role])]
print('Бот запущен')

morph = pymorphy2.MorphAnalyzer()
