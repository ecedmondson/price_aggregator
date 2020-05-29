from flaskext.mysql import MySQL
from pymysql.err import InternalError, OperationalError, ProgrammingError
from passlib.context import CryptContext

#Available functions:
#--------------------
#dbConfig(app, user, password, host = "classmysql.engr.oregonstate.edu", dbName = None)
#createTables()
#index(query)
#add(query)
#insertCustomer(f_name, l_name, email, password, customer_id = None)
#insertRetailer(name, url, retailer_id = None)
#insertProduct(name, brand, manuf_model, product_id = None)
#updateDatabaseProducts(products)
#getCustomers()
#getProducts()
#getProductsByName(name)
#getProductsByRetailer(retailerName)
#getRetailers()
#getRetailers_Products()
#findCustomer(email, password)

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
)

class Database():

    #To initialize the DB instance, you should only really need to pass the app, user, and password.
    def __init__(self, app, user, password, host = "classmysql.engr.oregonstate.edu", dbName = None):
        
        self.app = app
        self.mysql = MySQL()
        self.mysql.init_app(self.app)
        self.numberOfTables = 4

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

        #Checks to see if all 4 tables are in the database
        tables = self.index("show tables;")
        if(len(tables) != self.numberOfTables):
            self.createTables()


    #Sets up initial tables
    def createTables(self):
        #Set up connection
        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()
        except OperationalError:
            print("Cannot connect to MySQL server")
            print("Make sure you're connected to the VPN and the DB has benn configured correctly")
        except Exception as e:
            print("Could not connect to database")
            print(e)

        #Creates queries for each table
        createCustomers = "CREATE TABLE Customers (customer_id int NOT NULL, f_name varchar(255) NOT NULL,l_name varchar(255) NOT NULL, email varchar(255) NOT NULL, password varchar(255) NOT NULL, PRIMARY KEY(customer_id), UNIQUE KEY(email));"
        createProducts = "CREATE TABLE Products (product_id int, name varchar(255), PRIMARY KEY(product_id), UNIQUE KEY(name));"
        createRetailers = "CREATE TABLE Retailers (retailer_id int, name varchar(255), PRIMARY KEY(retailer_id), UNIQUE KEY(name));"
        createRetailers_Products = "CREATE TABLE Retailers_Products (product_id int, retailer_id int, name varchar(64), price varchar(32), photo varchar(255), source varchar(255), instock varchar(32), new varchar(32), price_check varchar(64), type varchar(64), PRIMARY KEY (product_id, retailer_id), FOREIGN KEY (product_id) REFERENCES Products(product_id), FOREIGN KEY (retailer_id) REFERENCES Retailers(retailer_id))"

        #Executes queries one table at a time
        try:
            cursor.execute(createCustomers)
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except InternalError:
            print("Customers table already exist")
        except Exception as e:
            print("Could not create table(s)")
            print(e)

        try:
            cursor.execute(createProducts)
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except InternalError:
            print("Products table already exist")
        except Exception as e:
            print("Could not create table(s)")
            print(e)

        try:
            cursor.execute(createRetailers)
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except InternalError:
            print("Retailers table already exist")
        except Exception as e:
            print("Could not create table(s)")
            print(e)

        try:
            cursor.execute(createRetailers_Products)
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except InternalError:
            print("Retailers_Products table already exist")
        except Exception as e:
            print("Could not create table(s)")
            print(e)

        conn.commit()
        return "Done"

    #Will return a tuple of tuples from the DB given a query string
    def index(self, query):
        #Sets up connection
        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()
        except OperationalError:
            print("Cannot connect to MySQL server")
            print("Make sure you're connected to the VPN and the DB has benn configured correctly")
        except Exception as e:
            print("Could not connect to database")
            print(e)

        #Executes query
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except ProgrammingError:
            print("Could not execute query: " + query)
            print("Make sure the table exists and spelling is correct")
        except Exception as e:
            print("Could not execute query")
            print(e)


    #Will insert into the DB given a query string
    def add(self, query):
        #Connect to database
        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()
        except OperationalError:
            print("Cannot connect to MySQL server")
            print("Make sure you're connected to the VPN and the DB has benn configured correctly")
        except Exception as e:
            print("Could not connect to database")
            print(e)

        #Executes query
        try:
            cursor.execute(query)
            conn.commit()
            return "Done"
        except UnboundLocalError:
            print("Error - Make sure you are correctly connected to the DB")
        except ProgrammingError:
            print("Improper query, make sure spelling and syntax is correct")
        except Exception as e:
            print("Could not execute query")
            print(e)

    #Inserts customer into database
    #Without a specific customer_id given, will generate one higher than last entry
    def insertCustomer(self, f_name, l_name, email, password, customer_id = None):
        if(customer_id == None):
            #Gets last customer entry and and sets the new customer_id one higher
            lastCust = self.index("SELECT * FROM Customers ORDER BY customer_id DESC")
            if (lastCust):
                customer_id = int(lastCust[0][0]) + 1
            else: 
                customer_id = 1

        #Hash password
        hashPass = pwd_context.encrypt(password)
        #Formulate query
        query = "INSERT INTO Customers (customer_id, f_name, l_name, email, password) VALUES (" + str(customer_id) + ",'" + str(f_name) + "','" + str(l_name) + "','" + str(email) + "','" + str(hashPass) + "');"
        #Send to DB
        self.add(query)


    #Checks DB to see if customer exists, 
    #If customer exists, returns their data, else if they don't exist, return nothing
    def findCustomer(self, email, password):
        query = "SELECT * FROM Customers WHERE email = '" + email + "';"
        result = self.index(query)
        if result:
            if(pwd_context.verify(password, result[0][4])):
                return result
            else:
                return None
        else:
            return None

    #If you want to add a retailer to the DB
    def insertRetailer(self, name, retailer_id = None):
        if(retailer_id == None):
            #Gets last retailer entry and and sets the new retailer_id one higher
            lastRetailer = self.index("SELECT * FROM Retailers ORDER BY retailer_id DESC")
            if (lastRetailer):
                retailer_id = int(lastRetailer[0][0]) + 1
            else: 
                retailer_id = 1

        #Forumlate query
        query = "INSERT INTO Retailers (retailer_id, name) VALUES (" + str(retailer_id) + ",'" + str(name) + "');"
        #Send to DB
        self.add(query)

    #If you want to add a product to the DB
    def insertProduct(self, name, product_id = None):
        if(product_id == None):
            lastProduct = self.index("SELECT * FROM Products ORDER BY product_id DESC")
            if (lastProduct):
                product_id = int(lastProduct[0][0]) + 1
            else: 
                product_id = 1

        #Formulate query
        query = "INSERT INTO Products (product_id, name) VALUES (" + str(product_id) + ",'" + str(name) + "');"
        #Send to DB
        self.add(query)
        
    def updateDatabaseProducts(self, products):
        try:
            for x in products:
                product = self.index("SELECT * FROM Products WHERE name='" + str(x.name) + "';")
                if not product:
                    self.insertProduct(x.name)
                    product = self.index("SELECT * FROM Products WHERE name='" + str(x.name) + "';")
                prodID = product[0][0]
                retailer = self.index("SELECT * FROM Retailers WHERE name='" + str(x.source) + "';")
                if not retailer:
                    self.insertRetailer(x.source)
                    retailer = self.index("SELECT * FROM Retailers WHERE name='" + str(x.source) + "';")
                retID = retailer[0][0]
                query = "REPLACE INTO Retailers_Products (product_id, retailer_id, name, price, photo, source, instock, new, price_check, type) VALUES (" + str(prodID) + "," + str(retID) + ",'" + str(x.name) + "','"+ str(x.price) +"','"+str(x.photo)+"','"+str(x.source)+"','"+str(x.instock)+"','"+str(x.new)+"','"+str(x.price_check)+"','" + str(x.product_type) + "');"
                self.add(query)
        except Exception as e:
            print(e)

    def getCustomers(self):
        query = "SELECT * FROM Customers"
        return self.index(query)

    def getProducts(self):
        query = "SELECT * FROM Products"
        return self.index(query)
    
    def getProductsByName(self, name):
        query = "SELECT * FROM Retailer_Products WHERE name='" + str(name) + "';"
        return self.index(query)
    
    def getProductsByRetailer(self, retailerName):
        query = "SELECT * FROM Retailer_Products WHERE source='" + str(retailerName) + "';"
        return self.index(query)

    def getRetailers(self):
        query = "SELECT * FROM Retailers"
        return self.index(query)

    def getRetailers_Products(self):
        query = "SELECT * FROM Retailers_Products"
        return self.index(query)