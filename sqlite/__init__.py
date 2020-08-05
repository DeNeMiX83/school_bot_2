from sqlite3 import connect

con = connect('sqlite\school.db')
cur = con.cursor()