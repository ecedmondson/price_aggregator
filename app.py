from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import Database
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from config import Config
from forms import SignUpForm

app = Flask(__name__)
app.config.from_object(Config)

db = Database(app, "cs361_alberjes", 3526)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
  def __init__(self,id):
    self.id = id

@app.route("/")
def home():
    print(db.findCustomer("hello123@gmail.com","12345678"))
    return render_template('home.html')

@app.route("/login")
def login():
    return "you are logged in"

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    print(request.method)
    if request.method == "POST":
        #add sign up logic
        if form.validate_on_submit():
            print("inside if")
            fname = form.fname.data
            lname = form.lname.data
            email = form.email.data
            password = form.password.data
            # Make sure user email isn't already in the database
            existing_user = db.findCustomer(email, password)
            print("existing_user %d", existing_user)
            if existing_user:
                flash('Email already exists, please log in or use a different email address.')
            else: 
                login_user(User(email))
                db.insertCustomer(fname, lname, email, password)
                flash('Login credentials received')
                return redirect(url_for('home'))
        else:
            print("validate failed", form.validate_on_submit())
    return render_template('signUp.html',
                            title='Create and Account.',
                            form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "you are logged out"

# Helper routes to make flask-login happy

# For every page load, app must verify that the user is logged in or not logged in
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    return User(user_id)

# Route for when user attempts to hit an unauthorized route in the app
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
