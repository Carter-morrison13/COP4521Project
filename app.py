from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)