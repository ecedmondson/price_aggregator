from flask import Flask, render_template
from database.db import Database
from flask_login import LoginManager
from forms import SignUpForm

app = Flask(__name__)
db = Database()
login_manager = LoginManager()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():

@app.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()
    if request.method == "POST"
        #add sign up logic
        if signup_form.validate_on_submit():
            fname = signup_form.get('fname')
            lname = signup_form.get('lname')
            email = signup_form.get('email')
            password = signup_form.get('password')
            
    return render_template("signUp.html",
                            title="Create and Account.",
                            form=SignUpForm(),
                            template="signup-page",
                            body="Sign up for a user account.")


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
