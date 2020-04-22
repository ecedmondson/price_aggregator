from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:admin:luckythirteen@softwareengineeringdb.clphunbfrcvm.us-east-1.rds.amazonaws.com:3306/sitedb'
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=9876, debug=True)
