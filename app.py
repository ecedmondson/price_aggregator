from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import Database
from flask_login import LoginManager
from config import Config
from forms import SignUpForm

app = Flask(__name__)
app.config.from_object(Config)

db = Database(app, "cs361_alberjes", 3526)
#db.createTables()
login_manager = LoginManager(app)

login_manager.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')

# @app.route("/login")
# def login():

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    print(request.method)
    if request.method == "POST":
        #add sign up logic
        if form.validate_on_submit():
            print("inside if")
            flash('Login credentials received')
            # fname = form.get('fname')
            # lname = form.get('lname')
            # email = form.get('email')
            # password = form.get('password')
            # existing_user = db.findCustomer(email, password)
            # print("existing_user %d", existing_user)
            return redirect(url_for('home'))
        else:
            print("validate failed", form.validate_on_submit())
    return render_template('signUp.html',
                            title='Create and Account.',
                            form=form)


# Helper routes to make flask-login happy

# For every page load, app must verify that the user is logged in or not logged in
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

# Route for when user attempts to hit an unauthorized route in the app
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

if __name__ == '__main__':
    app.run(debug=True)
