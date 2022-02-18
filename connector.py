import mysql.connector

# connect to sql in order to create the db
conn = mysql.connector.connect(
    host='localhost',
    # the user should default to root when you install it
    user='root',
    # this is the password I made it when installing mysql
    password='testing'
)

# create the db
conn_cursor = conn.cursor()
conn_cursor.execute("CREATE DATABASE shortstory_db")

# connect to the new db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='testing',
    database='shortstory_db'
)

cursor = db.cursor()
# create a 'users' table with the primary key as userID
cursor.execute('CREATE TABLE users (userID INT NOT NULL AUTO_INCREMENT, username VARCHAR(10), password VARCHAR(10), PRIMARY KEY (userID))')
print("Table created successfully")
db.close()
conn.close()



