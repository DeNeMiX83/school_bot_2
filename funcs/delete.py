from funcs.all_funcs import reset_role
from sqlite import cur, con


async def student_delete(student_id):
    cur.execute('''DELETE FROM students WHERE user = ?''', [student_id])
    con.commit()
    await reset_role(student_id)


async def classroom_delete(class_name):
    students_id = cur.execute('''SELECT user 
                                FROM students s
                                LEFT JOIN classes c ON c.id = s.class WHERE c.name = ?''',
                              [class_name]).fetchall()
    for student_id in students_id:
        await student_delete(student_id[0])
    cur.execute('''DELETE FROM classes WHERE name = ?''',
                [class_name])
    con.commit()