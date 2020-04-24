from flask import Flask, render_template
from db import *

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'cs361_bahorat'
app.config['MYSQL_DATABASE_PASSWORD'] = '1011'
app.config['MYSQL_DATABASE_DB'] = 'cs361_bahorat'
app.config['MYSQL_DATABASE_HOST'] = 'classmysql.engr.oregonstate.edu'

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
