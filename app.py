from collections import UserList
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from waitress import serve
app = Flask(__name__)
app.secret_key = 'your secret key'

class ChatroomClass:
    def __init__(self):
        self.userList = []
        self.turnToType = ''
        self.finishedTyping = []
        self.prompt = ''
        self.genre = ''
        self.story = ''


test = ChatroomClass()

@app.route('/')
def front_page():
    return render_template('frontPage.html')


@app.route('/adminPanel')
def admin_panel():
    if 'loggedin' not in session:
        return render_template('login_result.html', msg="You must be logged in to access the admin panel!")
    # check if user has correct role to create a prompt
    if session['role'] != 'admin':
        return render_template('login_result.html', msg="You must have the admin role to access the admin panel!")
    # if the role isn't allowed, we display the error message
    return render_template('adminPanel.html')


@app.route('/createPrompt')
def create_prompt():
    if 'loggedin' not in session:
        return render_template('login_result.html', msg="You must be logged in to create a prompt!")
    # check if user has correct role to create a prompt
    if session['role'] == 'Supporter':
        return render_template('createPrompt.html')
    # if the role isn't allowed, we display the error message
    return render_template('login_result.html', msg="You must be a Supporter to create a new prompt!")


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
        Role = 'default'

        # make sure form is filled out
        if Username == "" or Password == "":
            return render_template('login_result.html', msg="You must fill out every field in the form!")

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (Username, Password,))
        account = cursor.fetchone()
        if not account:
            sql = "INSERT INTO users (username, password, role, numStories) VALUES (%s,%s,%s,%s)"
            val = (Username, Password, Role, '0')
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
            # sets the session role to the role of the account
            session['role'] = account[2]
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

# route to display users profile
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
        role = account[2]
        # Show the profile page with account info
        return render_template('profile.html', username=username, password=password, role=role)

    # redirect to the login page if the user is not logged in
    return render_template('login.html')

# route to display leaderboard of users with most stories contributed to.
@app.route('/shortstory_db/leaderboards')
def leaderboard():
    # user does not need to be logged in to view the leaderboards
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='testing',
        database='shortstory_db'
    )
    # need to select all users and order them by the number stories they have contributed to
    cursor = db.cursor()
    cursor.execute('SELECT username, numStories FROM users ORDER BY numStories DESC LIMIT 10')
    usersList = cursor.fetchall()
    for i in range(len(usersList)):
        usersList[i] = usersList[i] + (i+1,)
    #print(usersList)
    return render_template('leaderboards.html', usersList=usersList)

# route to the support page where a User can choose to be upgraded to supporter role
@app.route('/shortstory_db/support', methods=['POST', 'GET'])
def support():
    msg = ""
    if 'loggedin' in session:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
    cursor = db.cursor()
    if session['role'] == "Supporter":
        return render_template('support.html', msg="Already supporting!")
    if request.method == 'POST':
        answer = request.form['supportAns']
        if answer == 'yes':
            cursor.execute('UPDATE users SET role = "Supporter" WHERE username = %s', (session['username'],))
            db.commit()
            # sets the session role to the role of the account
            session['role'] = 'Supporter'
            msg = "Thank you for supporting! Role has been updated."
        else:
            msg = "Not supporting. Same role as before"
            return render_template('support.html', msg=msg)

    return render_template('support.html', msg=msg)


@app.route('/shortstory_db/browse')
def browse():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='testing',
        database='shortstory_db'
    )
    cursor = db.cursor()
    cursor.execute('SELECT story_name, story, author1, author2 FROM stories LIMIT 15')
    rows = cursor.fetchall()
    print(rows)
    #cur.execute("SELECT Username, Review, Rating FROM Reviews WHERE Restaurant = ?", (name,))

    return render_template('browse.html', ROWS=rows)


@app.route('/shortstory_db/moderate', methods=['POST', 'GET'])
def moderate():
    msg = ""
    if 'loggedin' in session:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
    else:
        msg = "Please log in"
        return render_template('moderate.html', msg = msg)
    cursor = db.cursor()
    if session['role'] == "Moderator":
        return render_template('moderate.html', msg="Already a mod!")
    if request.method == 'POST':
        answer = request.form['modAns']
        if answer == 'imamodnow':
            cursor.execute('UPDATE users SET role = "Moderator" WHERE username = %s', (session['username'],))
            db.commit()
            msg = "You are now a moderator! Please moderate with responsibility."
        else:
            msg = "The password is incorrect"
            
    return render_template('moderate.html', msg = msg)

@app.route("/shortstory_db/chatroom", methods=["POST", "GET"])
def chatroom():
    if len(test.userList) == 0:
        test.userList.append(session['username'])
        if test.turnToType == '':
            test.turnToType = test.userList[0]
        return redirect('/shortstory_db/chatroomSetup')

    if session['username'] not in test.userList:
        test.userList.append(session['username'])
    while test.prompt == '':
        return render_template('waitingRoom.html')


    doneTyping = 'no'
    if request.method == 'POST':
        test.story += request.form['StoryBox']
        doneTyping = request.form.get('done')

    if (request.method == 'POST') and (not (session['username'] in test.finishedTyping)):
        print(len(test.finishedTyping))
        if len(test.finishedTyping) == 0:
            if test.turnToType is test.userList[0]:
                test.turnToType = test.userList[1]
            else:
                test.turnToType = test.userList[0]

    if doneTyping == 'yes' and not session['username'] in test.finishedTyping:
        test.finishedTyping.append(session['username'])

    if len(test.finishedTyping) == 2 and test.userList[0] == session['username']:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
        # update the stories table with this new story
        cursor = db.cursor()
        sql = "INSERT INTO stories (story_name, prompt, author1, author2, story) VALUES (%s,%s,%s,%s,%s)"
        val = (storyName, test.prompt, test.userList[0], test.userList[1], test.story)
        cursor.execute(sql, val)
        db.commit()
        # update each of the two users 'numStories' field in the users table
        cursor = db.cursor()
        sql = "UPDATE users SET numStories = numStories + 1 WHERE username='" + test.userList[0] + "'"
        cursor.execute(sql)
        db.commit()
        cursor = db.cursor()
        sql = "UPDATE users SET numStories = numStories + 1 WHERE username='" + test.userList[1] + "'"
        cursor.execute(sql)
        db.commit()   
        test.userList = []
        test.turnToType = ''
        test.finishedTyping = []
        test.prompt = ''
        test.genre = ''
        test.story = ''
        return render_template('finishedScreen.html', story=test.story)

    elif len(test.finishedTyping) == 2 and test.userList[1] == session['username']:
        return render_template('finishedScreen.html', story=test.story)

    if session['username'] in test.finishedTyping:
        return render_template('chatroom.html', username=session['username'], chatList=test.userList,
                               story=test.story, prompt=test.prompt,
                               typingTurn=test.turnToType, allowed='no')
    if session['username'] == test.turnToType:
        return render_template('chatroom.html', username=session['username'], chatList=test.userList, story=test.story,
                               prompt=test.prompt, typingTurn=test.turnToType, allowed='yes')
    else:
        return render_template('chatroom.html', username=session['username'], chatList=test.userList, story=test.story,
                               prompt=test.prompt, typingTurn=test.turnToType, allowed='no')

@app.route("/shortstory_db/chatroomSetup", methods=["POST", "GET"])
def chatroomSetup():
    if request.method == 'GET':
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testing',
            database='shortstory_db'
        )
        cursor = db.cursor()
        cursor.execute('SELECT prompt, genre FROM storage')
        prompt = cursor.fetchall()
        return render_template('chatroomSetup.html', prompt=prompt)
    elif request.method == 'POST':
        prompt = request.form['prompt']
        test.prompt = prompt
        global storyName
        storyName = request.form['storyName']
        return redirect('/shortstory_db/chatroom')


if __name__ == '__main__':
    #app.run(debug=True)
    serve(app, host="0.0.0.0", port=5000, threads=8)
