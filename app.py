from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:bahorat-db:RHvPQdC1JiKCStjg@oniddb.cws.oregonstate.edu:3306/bahorat-db'
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
