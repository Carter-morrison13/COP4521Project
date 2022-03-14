from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'


@app.route('/')
def front_page():
    return render_template('frontPage.html')


@app.route('/createPrompt')
def create_prompt():
    if 'loggedin' not in session:
        return render_template('login_result.html', msg="You must be logged in to create a prompt!")
    return render_template('createPrompt.html')


@app.route('/create_Prompt', methods=['POST', 'GET'])
def create_prompt_function():
    if request.method == 'POST':
        # connect to the db
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
        prompt = request.form['prompt']
        genre = request.form['genre']

        # make sure form is filled out
        if prompt == "" or genre == "":
            return render_template('login_result.html', msg="You must fill out every field in the form!")

        cursor = db.cursor()
        cursor.execute('SELECT * FROM storage WHERE prompt = %s', (prompt,))
        account = cursor.fetchone()
        if not account:
            sql = "INSERT INTO storage (prompt, genre) VALUES (%s,%s)"
            val = (prompt, genre)
            cursor.execute(sql, val)
            db.commit()
            return render_template('login_result.html', msg="Successfully created Prompt!")
        else:
            return render_template('login_result.html', msg="Error creating Prompt!")


@app.route('/createAccount')
def create_account():
    if 'loggedin' in session:
        return render_template('login_result.html', msg="You are already logged into an account!")
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
        Username = request.form['username']
        Password = request.form['password']

        # make sure form is filled out
        if Username == "" or Password == "":
            return render_template('login_result.html', msg="You must fill out every field in the form!")

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (Username, Password,))
        account = cursor.fetchone()
        if not account:
            sql = "INSERT INTO users (Username, password) VALUES (%s,%s)"
            val = (Username, Password)
            cursor.execute(sql, val)
            db.commit()
            return render_template('login_result.html', msg="Successfully created account!")
        else:
            return render_template('login_result.html', msg="Error creating account!")


@app.route('/login')
def login():
    if 'loggedin' in session:
        return render_template('login_result.html', msg="You are already logged into an account!")
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
            # sets the session username to the username of the account
            session['username'] = account[0]
            # Redirect to profile page after logging in
            return profile()
        else:
            msg = 'Invalid Credentials!'
            return render_template("login_result.html", msg=msg)


@app.route('/shortstory_db/logout')
def logout():
    # if user is logged in to an account currently
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('username', None)
        return render_template("login_result.html", msg="Successfully logged out!")

    # if user is not logged in to an account
    return render_template('login_result.html', msg="You are not logged in to an account!")


@app.route('/shortstory_db/profile')
def profile():
    # make sure user is currently logged in
    if 'loggedin' in session:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (session['username'],))
        account = cursor.fetchone()
        username = account[0]
        password = account[1]
        # Show the profile page with account info
        return render_template('profile.html', username=username, password=password)

    # redirect to the login page if the user is not logged in
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
