from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import Database
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from config import Config
from forms import SignUpForm, LoginForm
from assets.scraped_product import ScrapedProduct
from assets.product_interface import ProductInterface

app = Flask(__name__)
app.config.from_object(Config)

db = Database(app, "cs361_xxxxxxx", 'xxxx')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
  def __init__(self,id):
    self.id = id

backend = ProductInterface()

@app.route("/")
def home():
    print(db.findCustomer("hello123@gmail.com","12345678"))
    return render_template('home.html')


@app.route("/resources/products", methods=["POST"])
def search_products_api(**kwargs):
    if request.method == 'POST':
        return { f"{x['source'].lower()}_{x['name'].lower().replace(' ', '_')}": x for x in backend.get_products_by_filters(json=True, **request.json)}


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        #add sign in logic
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # Make sure user email is already in the database
            existing_user = db.findCustomer(email, password)
            if existing_user:
                login_user(User(email))
                flash('Login credentials received')
                return redirect(url_for('home'))
            else: 
                flash('Email does not exist. Please create an account.')
    return render_template('login.html',
                            title='Log into Existing Account.',
                            form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    print(request.method)
    if request.method == "POST":
        #add sign up logic
        if form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data
            email = form.email.data
            password = form.password.data
            # Make sure user email isn't already in the database
            existing_user = db.findCustomer(email, password)
            if existing_user:
                flash('Email already exists, please log in or use a different email address.')
            else: 
                login_user(User(email))
                db.insertCustomer(fname, lname, email, password)
                flash('Login credentials received')
                return redirect(url_for('home'))
    return render_template('signUp.html',
                            title='Create and Account.',
                            form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.')
    return render_template('home.html')

# Functions required for user-login
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


class ProductDBInterface:
    def parse_sql_tuple(self, x):
        return (ScrapedProduct(name = x[2], source = x[5], price = x[3], photo = x[4], instock= x[6], new = x[7], price_check= x[8]))

    def read_products_from_db(self):
        prod_tuple = db.getRetailers_Products()
        products = [self.parse_sql_tuple(x) for x in prod_tuple]
        return products

interface = ProductDBInterface()

@app.route("/listings")
def listings():
    return render_template('listings.html', items=interface.read_products_from_db())

if __name__ == '__main__':
    app.run()
