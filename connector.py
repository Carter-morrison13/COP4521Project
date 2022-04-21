import mysql.connector
# Database management program (mostly for testings and makes removing tables and the db itself easy)
# The prompt function is at the very bottom of this file
# You must edit the password field below wherever it is used to match your mysql server password that you set when you
# installed mysql.


# connect to sql server in order to create the db (need to have mysql server installed)
conn = mysql.connector.connect(
    host='localhost',
    # the user should default to root when you install it
    user='root',
    # this is the password I made it when installing mysql
    password='testing'
)


def create_db():
    try:
        # create the db
        conn_cursor = conn.cursor()
        conn_cursor.execute("CREATE DATABASE shortstory_db")
        print("Database created successfully!")
    except:
        print("Database already exists!")


def create_tables():
    # connect to the db
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
    except:
        print("Database does not exist!")
        return

    cursor = db.cursor()
    # create the tables
    try:
        cursor.execute(
            'CREATE TABLE users (username VARCHAR(20) NOT NULL UNIQUE, password VARCHAR(100) NOT NULL, role VARCHAR(20) NOT NULL, numStories INTEGER, PRIMARY KEY (username))')
        cursor.execute(
            'CREATE TABLE storage (prompt VARCHAR(25) NOT NULL UNIQUE, genre VARCHAR(10) NOT NULL, PRIMARY KEY (prompt))')
        cursor.execute(
            'CREATE TABLE stories (story_name VARCHAR(25) NOT NULL UNIQUE, prompt VARCHAR(25) NOT NULL UNIQUE, author1 VARCHAR(10) NOT NULL, author2 VARCHAR(10) NOT NULL, story TEXT NOT NULL, ratings INTEGER NOT NULL, PRIMARY KEY (story_name), FOREIGN KEY (prompt) REFERENCES storage(prompt))')
        print("Tables created successfully!")
        db.close()
    except:
        print("Tables already exist!")
        db.close()


def drop_db():
    try:
        # drop the db
        conn_cursor = conn.cursor()
        conn_cursor.execute("DROP DATABASE shortstory_db")
        print("Database dropped successfully!")
    except:
        print("Database doesn't exist!")


def drop_tables():
    # connect to the db
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='shortstory_db'
        )
    except:
        print("Database does not exist!")
        return

    cursor = db.cursor()
    # drop the tables
    try:
        cursor.execute('DROP TABLE users')
        cursor.execute('DROP TABLE stories')
        cursor.execute('DROP TABLE storage')
        print("Tables dropped successfully!")
        db.close()
    except:
        print("Table already exists!")
        db.close()


while True:
    choice = (input("Choose from the below options:\n"
                    "1. Create the database\n"
                    "2. Create the tables\n"
                    "3. Drop the database\n"
                    "4. Drop the tables\n"
                    "5. Exit\n"))
    if choice == str(1):
        create_db()
    elif choice == str(2):
        create_tables()
    elif choice == str(3):
        drop_db()
    elif choice == str(4):
        drop_tables()
    elif choice == str(5):
        quit()
    else:
        print("Invalid input")




