from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/base.html')
def render_webpage():  # put application's code here
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
