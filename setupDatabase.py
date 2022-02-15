import sqlite3

conn = sqlite3.connect('webDatabase.db')

conn.execute('CREATE TABLE LoginInfo (Username TEXT, Password TEXT)')