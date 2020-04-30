from flaskext.mysql import MySQL

#Available functions:
#dbConfig(app, user, password, host = "classmysql.engr.oregonstate.edu", dbName = None)
#dbInitialize(app)
#dbIndex(app, query)
#dbAdd(app, query)
#insertCustomer(app, f_name, l_name, email, password, customer_id = None)
#findCustomer(app, email, password)


#Configures app to work with your DB
#Should only need to pass arguments 'app, user, password' for our purposes
def dbConfig(app, user, password, host = "classmysql.engr.oregonstate.edu", dbName = None):

    if(dbName == None):
        dbName = user

    try:
        #Username = cs361_*username* (eg. cs361_bahorat)
        app.config['MYSQL_DATABASE_USER'] = str(user)
        #Password = Last 4 of your student number (eg. 1011)
        app.config['MYSQL_DATABASE_PASSWORD'] = str(password)
        #Host = classmysql.engr.oregonstate.edu
        app.config['MYSQL_DATABASE_HOST'] = str(host)
        #DbName = Defualts to same as username
        app.config['MYSQL_DATABASE_DB'] = str(dbName)
    except Exception as e:
        print("Could not configure app to connect to database")
        print(e)


#Sets up initial tables
def dbInitialize(app):
    #Set up connection
    try:
        mysql = MySQL()
        mysql.init_app(app)

        conn = mysql.connect()
        cursor = conn.cursor()
    except Exception as e:
        print("Could not connect to database")
        print(e)

    #Cretes queries for each table
    createCustomers = "CREATE TABLE Customers (customer_id int NOT NULL, f_name varchar(255) NOT NULL,l_name varchar(255) NOT NULL, email varchar(255) NOT NULL, pass varchar(255) NOT NULL, PRIMARY KEY(customer_id), UNIQUE KEY(email));"
    createProducts = "CREATE TABLE Products (product_id int, name varchar(255), brand varchar(255), manuf_model varchar(255), PRIMARY KEY(product_id));"
    createRetailers = "CREATE TABLE Retailers (retailer_id int, name varchar(255), url varchar(255), PRIMARY KEY(retailer_id));"

    #Executes queries
    try:
        cursor.execute(createCustomers)
        cursor.execute(createProducts)
        cursor.execute(createRetailers)
        conn.commit()
        return "Done"
    except Exception as e:
        print("Could not create table(s)")
        print(e)
        return "Error"

#Will return a tuple of tuples from the DB given a query string
def dbIndex(app, query):
    #Sets up connection
    try:
        mysql = MySQL()
        mysql.init_app(app)

        conn = mysql.connect()
        cursor = conn.cursor()
    except Exception as e:
        print("Could not connect to database")
        print(e)

    #Executes query
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Could not execute query")
        print(e)


#Will insert into the DB given a query string
def dbAdd(app, query):
    #Connect to database
    try:
        mysql = MySQL()
        mysql.init_app(app)

        conn = mysql.connect()
        cursor = conn.cursor()
    except Exception as e:
        print("Could not connect to database")
        print(e)
        
    #Executes query
    try:
        cursor.execute(query)
        conn.commit()
        return "Done"
    except Exception as e:
        print("Could not execute query")
        print(e)


#Inserts customer into database
#Without a specific customer_id given, will generate one higher than last entry
def insertCustomer(app, f_name, l_name, email, password, customer_id = None):
    #Gets last customer entry and and sets the new customer_id one higher
    lastCust = dbIndex(app, "SELECT * FROM Customers")
    if (lastCust):
        customer_id = int(lastCust[0][0]) + 1
    else: 
        customer_id = 1

    #Formulate query
    query = "INSERT INTO Customers (customer_id, f_name, l_name, email, pass) VALUES (" + str(customer_id) + ",'" + str(f_name) + "','" + str(l_name) + "','" + str(email) + "','" + str(password) + "');"
    #Send to DB
    dbAdd(app, query)


#Checks DB to see if customer exists, 
#If customer exists, returns their data, else if they don't exist, return nothing
def findCustomer(app, email, password):
    query = "SELECT * FROM Customers WHERE email = '" + email + "' AND pass = '" + password +"';"
    return dbIndex(app, query)