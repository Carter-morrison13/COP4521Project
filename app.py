from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/')
def front_page():
    return render_template('frontPage.html')


@app.route('/createAccount')
def create_account():
    return render_template('createAccount.html')


@app.route('/create_Account', methods=['POST', 'GET'])
def create_function():
    if request.method == 'POST':

        # connect to the db
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )

        try:
            Username = request.form['username']
            Password = request.form['password']
            cursor = db.cursor()
            sql = "INSERT INTO users (Username, password) VALUES (%s,%s)"
            val = (Username, Password)
            cursor.execute(sql, val)
            db.commit()

        except:
            # rollback if unable to insert correctly
            db.rollback()

        finally:
            db.close()
            return render_template("frontPage.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login_function', methods=['POST', 'GET'])
def login_function():

    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # connect to the db
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        # if corresponding account exists in the db
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # setts the session username to the username of the account
            session['username'] = account[0]
            # Redirect to home page
            msg = 'Logged in successfully!'
            return render_template("login_result.html", msg=msg)
        else:
            msg = 'Invalid Credentials!'
            return render_template("login_result.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
