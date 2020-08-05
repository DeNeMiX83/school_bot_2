import os

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
teacher_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                              [teacher_role])]
student_id_list = [user[0] for user in cur.execute('''SELECT user_id FROM users WHERE role = ?''',
                                              [student_role])]
print(admin_id_list, director_id_list, teacher_id_list, student_id_list)
ip = os.getenv("ip")


aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
