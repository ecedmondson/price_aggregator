from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'cs361_bahorat'
app.config['MYSQL_DATABASE_PASSWORD'] = '1011'
app.config['MYSQL_DATABASE_DB'] = 'cs361_bahorat'
app.config['MYSQL_DATABASE_HOST'] = 'classmysql.engr.oregonstate.edu'

@app.route("/")
def home():
    return render_template('home.html')

#Will return a tuple from the DB given a query string
def dbIndex(query):
    mysql = MySQL()
    mysql.init_app(app)

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    return data
    
#Will insert into the DB given a query string
def dbAdd(query):
    mysql = MySQL()
    mysql.init_app(app)

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute(query)
    conn.commit()
    return "Done"

if __name__ == '__main__':
    app.run(debug=True)
