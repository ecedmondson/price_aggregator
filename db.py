from flaskext.mysql import MySQL

#Will return a tuple from the DB given a query string
def dbIndex(app, query):
    mysql = MySQL()
    mysql.init_app(app)

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute(query)
    data = cursor.fetchall()
    return data
    
#Will insert into the DB given a query string
def dbAdd(app ,query):
    mysql = MySQL()
    mysql.init_app(app)

    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute(query)
    conn.commit()
    return "Done"