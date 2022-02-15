from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
@app.route('/')

def frontPage():
    return render_template('frontPage.html')

@app.route('/login')

def loginFunct():
    return render_template('login.html')

@app.route('/about')

def aboutFunct():
    return render_template('about.html')

if __name__ =='__main__':
    app.run()