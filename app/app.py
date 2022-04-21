import hashlib
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import time
#from waitress import serve

app = Flask(__name__)
app.secret_key = 'your secret key'

class ChatroomClass:
    def __init__(self):
        self.userList = []
        self.turnToType = ''
        self.finishedTypingList = []
        self.prompt = ''
        self.genre = ''
        self.story = ''
        self.storyName = ''

# dictionary/map of the current stories where key is the  going on
chatrooms_map = {}

# global for the waiting users
waiting_users = []

# get chatroom for a specific user by their username using the fact
# the user will be in the chatrooms userList
def getChatroomByUser(user):
    for chatroom_key in chatrooms_map:
        chatroom = chatrooms_map[chatroom_key]
        print(user)
        print(chatroom.userList)
        if user in chatroom.userList:
            return chatroom
    return None


# function to get a db connection
# change password to match yours
def getDbConnection():
    return mysql.connector.connect(
            host='db',
            user='root',
            password='testing',
            database='shortstory_db'
        )

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

@app.route('/voting')
def voting():
    if 'loggedin' not in session:
        return render_template('login_result.html', msg="You must be logged in to cast a vote!")
    # check if user has correct role to create a prompt
    if session['role'] == 'Supporter' or session['role'] == 'Moderator' or session['role'] == 'default':
        return render_template('voting.html')
    # if the role isn't allowed, we display the error message
    return render_template('login_result.html', msg="You must be a Supporter to create a new prompt!")

@app.route('/cast_vote', methods=['POST', 'GET'])
def cast_vote_func():
    if request.method == 'POST':
        db = getDbConnection()
        name = request.form['storyname']
        cur = db.cursor()
        cur.execute('SELECT * FROM stories WHERE story_name = %s', (name,))
        check = cur.fetchone()
        if check:
            cur.execute('UPDATE stories ratings SET ratings = ratings + 1 WHERE story_name = %s', (name,))
            db.commit()
            return render_template('login_result.html', msg="Succesfully cast your vote!")
        else:
            return render_template('login_result.html', msg="Story was not found.")

@app.route('/create_Prompt', methods=['POST', 'GET'])
def create_prompt_function():
    if request.method == 'POST':
        # connect to the db
        db = getDbConnection()
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
        db = getDbConnection()
        Username = request.form['username']
        Password = request.form['password']
        Role = 'default'

        # make sure form is filled out
        if Username == "" or Password == "":
            return render_template('login_result.html', msg="You must fill out every field in the form!")

        # encrpyting the password with SHA256
        Password = Password.encode('utf-8')
        Password = hashlib.sha256(Password).hexdigest()

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
        db = getDbConnection()

        # encrpyting the password with SHA256
        password = password.encode('utf-8')
        password = hashlib.sha256(password).hexdigest()

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
        db = getDbConnection()
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
    db = getDbConnection()
    # need to select all users and order them by the number stories they have contributed to
    cursor = db.cursor()
    cursor.execute('SELECT username, numStories FROM users ORDER BY numStories DESC LIMIT 10')
    usersList = cursor.fetchall()
    for i in range(len(usersList)):
        usersList[i] = usersList[i] + (i + 1,)
    # print(usersList)
    return render_template('leaderboards.html', usersList=usersList)


# route to the support page where a User can choose to be upgraded to supporter role
@app.route('/shortstory_db/support', methods=['POST', 'GET'])
def support():
    msg = ""
    if 'loggedin' in session:
        db = getDbConnection()
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
    db = getDbConnection()
    cursor = db.cursor()
    cursor.execute('SELECT story_name, story, author1, author2, ratings FROM stories LIMIT 15')
    rows = cursor.fetchall()
    #print(rows)
    # cur.execute("SELECT Username, Review, Rating FROM Reviews WHERE Restaurant = ?", (name,))

    return render_template('browse.html', ROWS=rows)


@app.route('/shortstory_db/moderate', methods=['POST', 'GET'])
def moderate():
    msg = ""
    if 'loggedin' in session:
        db = getDbConnection()
    else:
        msg = "Please log in"
        return render_template('moderate.html', msg=msg)
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

    return render_template('moderate.html', msg=msg)


@app.route('/shortstory_db/chatroomChoice', methods=["POST", "GET"])
def chatroomChoice():
    return render_template('chatroomChoice.html')

# function to implement users waiting in waiting room
# essentially every 1s checks for open chat rooms and when one is open
# they will be moved to this chatroom
@app.route("/shortstory_db/waitingRoom", methods=["POST", "GET"])
def waitingRoom():
    # get current user and append to the waiting users queue
    currentUser = session["username"]
    
    # now get the chatroom for this user and use it to redirect to the chatroom for his story
    chatroom = getChatroomByUser(currentUser)
    if chatroom != None:
        return redirect('/shortstory_db/chatroom_'+chatroom.storyName)

    global waiting_users
    waiting_users.append(currentUser)
    # while the current user is still in waiting users
    while currentUser in waiting_users:
        # want to pop the front waiting user
        for chatroom_key in chatrooms_map:
            chatroom = chatrooms_map[chatroom_key]
            if len(chatroom.userList) == 1:
                front_user = waiting_users[0]
                # add this user to the chatroom
                chatroom.userList.append(front_user)
                # remove this user from waiting users
                waiting_users.remove(front_user)
        time.sleep(1)
        return render_template('waitingRoom.html')
    
    # now get the chatroom for this user and use it to redirect to the chatroom for his story
    chatroom = getChatroomByUser(currentUser)
    return redirect('/shortstory_db/chatroom_'+chatroom.storyName)

# route for the chat room functionality
@app.route("/shortstory_db/chatroom_<storyName>", methods=["POST", "GET"])
def chatroom(storyName):
    chatroom = chatrooms_map[storyName]

    currentUser = session['username']

    # wait until the second user joins the chatroom
    while len(chatroom.userList) < 2:
        time.sleep(1)
        render_template('chatroom.html', username=currentUser, chatList=chatroom.userList, story=chatroom.story,
                               prompt=chatroom.prompt, typingTurn=chatroom.turnToType, allowed='no', storyName=storyName)

    # now while the two users are not done typing we continually do POST
    # requests each time the user's go to this page
    doneTyping = 'no'

    # if method is POST, then get whats in the story box
    # and then get if this user is done.
    if request.method == 'POST':
        chatroom.story += request.form['StoryBox']
        doneTyping = request.form.get('done')

    # if method is POST and the current user is not finished typing
    if (request.method == 'POST') and (not (currentUser in chatroom.finishedTypingList)):
        print(len(chatroom.finishedTypingList)) # print the length of finished typing
        
        # if length of finished typing is 0   
        if len(chatroom.finishedTypingList) == 0:
            # check whose turn it is to type and then switch whose turn
            if chatroom.turnToType is chatroom.userList[0]:
                chatroom.turnToType = chatroom.userList[1]
            else:
                chatroom.turnToType = chatroom.userList[0]

    # if current user is done typing and is not in the finished typing array of users
    # append current user to finished typing
    if doneTyping == 'yes' and not currentUser in chatroom.finishedTypingList:
        chatroom.finishedTypingList.append(currentUser)

    # when length of finished typing is 2 and the the first user in userList is the current user
    if len(chatroom.finishedTypingList) == 2 and chatroom.userList[0] == currentUser:
        db = getDbConnection()
        # update the stories table with this new story
        cursor = db.cursor()
        sql = "INSERT INTO stories (story_name, prompt, author1, author2, story, ratings) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (chatroom.storyName, chatroom.prompt, chatroom.userList[0], chatroom.userList[1], chatroom.story, '0')
        cursor.execute(sql, val)
        db.commit()
        # update each of the two users 'numStories' field in the users table
        cursor = db.cursor()
        sql = "UPDATE users SET numStories = numStories + 1 WHERE username='" + chatroom.userList[0] + "'"
        cursor.execute(sql)
        db.commit()
        cursor = db.cursor()
        sql = "UPDATE users SET numStories = numStories + 1 WHERE username='" + chatroom.userList[1] + "'"
        cursor.execute(sql)
        db.commit()
        tmp = chatroom.story
        # now delete this chatroom from our map of current chatrooms/stories
        del chatrooms_map[chatroom.storyName]

        return render_template('finishedScreen.html', story=tmp)

    # else if finished typing list is length 2 and user 1 in the user list is the current user
    elif len(chatroom.finishedTypingList) == 2 and chatroom.userList[1] == session['username']:
        # return the finished screen
        return render_template('finishedScreen.html', story=chatroom.story)

    # if the current user is in the finished test list, then they are the first one to finish
    if session['username'] in chatroom.finishedTypingList:
        return render_template('chatroom.html', username=session['username'], chatList=chatroom.userList,
                               story=chatroom.story, prompt=chatroom.prompt,
                               typingTurn=chatroom.turnToType, allowed='no', storyName=storyName)

     # if its the current users turn to type
    if session['username'] == chatroom.turnToType:
        # render the chatroom with current info where they can type
        return render_template('chatroom.html', username=session['username'], chatList=chatroom.userList, story=chatroom.story,
                               prompt=chatroom.prompt, typingTurn=chatroom.turnToType, allowed='yes', storyName=storyName)
    # else return them the chatroom where they cant type with the current info
    else:
        return render_template('chatroom.html', username=session['username'], chatList=chatroom.userList, story=chatroom.story,
                               prompt=chatroom.prompt, typingTurn=chatroom.turnToType, allowed='no', storyName=storyName)


# route for when a user goes to the chatroom setup. First user to join the chat room
# will be sent to this page
@app.route("/shortstory_db/chatroomSetup", methods=["POST", "GET"])
def chatroomSetup():
    # case 1. Its a GET request
    if request.method == 'GET':
        # get connection to database
        db = getDbConnection()
        # get connection to database
        cursor = db.cursor()
        # execute SELECT query to get the current prompts and genres to display to the user
        cursor.execute('SELECT prompt, genre FROM storage')
        # TODO: get the genre as well
        prompt = cursor.fetchall()
        print(prompt)
        return render_template('chatroomSetup.html', prompt=prompt)
    elif request.method == 'POST':
        # case 2. POST request
        # get the user selected prompt and story name
        prompt = request.form['prompt']
        print('received prompt: {0}'.format(prompt))
        #prompt = prompt[0]
        #genre = prompt[1]
        # store storyName as a global
        storyName = request.form['storyName']
        # create a new chatroom in the map
        chatroom = ChatroomClass()
        # set the prompt
        chatroom.prompt = prompt
        #chatroom.genre = genre
        # add current user to the user list for this chatroom
        chatroom.userList.append(session['username'])
        chatroom.storyName = storyName
        chatroom.turnToType = session['username']
        # chatrooms map key 'storyName' now points to this new chatroom object
        chatrooms_map[storyName] = chatroom

        return redirect('/shortstory_db/chatroom_'+storyName)

if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host="0.0.0.0", port=5000, threads=8)
