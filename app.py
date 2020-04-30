from flask import Flask, render_template
from db import *

app = Flask(__name__)

dbConfig(app, "cs361_bahorat", "1011")
initializeDb(app)
insertCustomer(app, "Tanner", "Bahora", "tan@fna", "pass")

data = findCustomer(app, "sdf@fds", "pass")
print(data)

@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
