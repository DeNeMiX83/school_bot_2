from sqlite3 import connect

con = connect('school.db')
cur = con.cursor()