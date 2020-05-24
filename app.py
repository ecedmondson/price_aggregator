from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import Database
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_login import AnonymousUserMixin
from config import Config
from forms import SignUpForm, LoginForm
from assets.scraped_product import ScrapedProduct
from datetime import datetime
from itertools import chain

##############
# APP CONFIG #
##############

app = Flask(__name__)
app.config.from_object(Config)

db = Database(app, "cs361_bahorat", '1011')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

###############
# USER CONFIG #
###############

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Guest'

login_manager.anonymous_user = Anonymous

class User(UserMixin):
  def __init__(self, id):
    self.id = id
    self.query = db.touch_id(id)
    self.first = self.query[0][1] if self.query else None
    self.last = self.query[0][2] if self.query else None
    self.name = f"{self.first} {self.last}" if self.query else 'Guest'
    self.email = self.query[0][3] if self.query else None
    self.timestamp = datetime.now().isoformat()


#####################
# PRODUCT INTERFACE #
#####################

def list_from(item):
    if not item:
        return []
    if isinstance(item, (str, dict)) or not is_iterable(
        item
    ):
        return [item]
    return list(item)


class ProductDBInterface:
    """Interface object so that the UI can easily obtain filtered products."""
    def parse_sql_tuple(self, x):
        return (ScrapedProduct(name = x[2], source = x[5], price = x[3], photo = x[4], instock= x[6], new = x[7], price_check= x[8]))

    @property
    def read_products_from_db(self):
        prod_tuple = db.getRetailers_Products()
        products = [self.parse_sql_tuple(x) for x in prod_tuple]
        return products


    def filter_products(self, json=False, product_type=None, sources_to_exclude=None, price_ceiling=None, use_status=None):
        """Pass filters as kwargs
        
        Filter options:
            - product_type (str): 'computer' or 'tablet'
            - sources_to_exclude (str): a retailer, i.e. 'amazon'
            - price_ceiling (int): highest price
            - use_status (str): use status, i.e. new or used
        """
        all_products = self.read_products_from_db
        product_type = list_from(product_type) or []
        sources_to_exclude = list_from(sources_to_exclude) or []
        price_ceiling = price_ceiling or 0
        use_status = list_from(use_status) or []
        # List typecast since chain is consumed upon iteration
        exclude = list(chain(product_type, sources_to_exclude, use_status))

        def desirable(product):
            """Takes a ScrapedProduct object and returns user-desirability boolean."""
            prod_chars = [getattr(product, x) for x in ["source", "price_n", "new"]]
            exclusion_matches = [
                x in exclude if not isinstance(x, int) else x < price_ceiling
                for x in prod_chars
            ]
            return any(exclusion_matches)

        filtered = list(filter(lambda p: not desirable(p), all_products))
        print(filtered)
        if json:
            return [x.jsonify() for x in filtered]
        return filtered

interface = ProductDBInterface()

##########
# ROUTES #
##########

@app.route("/")
def home():
    return render_template('home.html')

def unique_json_key(p):
    """Returns a unique JSON Key based on ScrapedProduct data. Takes a JSON blob/dict."""
    return f"{x['source'].lower()}_{x['name'].lower().replace(' ', '_')}"

@app.route("/resources/products", methods=["POST"])
def search_products_api(**kwargs):
    if request.method == 'POST':
        return { unique_json_key(x): x for x in interface.filter_products(json=True, **request.json)}


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
                print(existing_user)
                login_user(User(existing_user[0][0]))
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
                db.insertCustomer(fname, lname, email, password)
                existing_user = db.findCustomer(email, password)
                login_user(User(existing_user[0][0]))
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


@app.route("/listings")
@login_required
def listings():
    return render_template('listings.html', items=interface.filter_products())

# if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=4740)

