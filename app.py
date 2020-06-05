from flask import Flask, render_template, request, flash, redirect, url_for
from database.db import Database
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from config import Config
from forms import SignUpForm, LoginForm
from assets.scraped_product import ScrapedProduct
from itertools import chain

app = Flask(__name__)
app.config.from_object(Config)

db = Database(app, "cs361_alberjes", '3526')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
  def __init__(self,id):
    self.id = id


#####################
# PRODUCT INTERFACE #
#####################
def is_iterable(item):
    try:
        iter(item)
        return True
    except TypeError:
        return False


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
        return (ScrapedProduct(msrp = x[4], name = x[2], source = x[6], price = x[3], product_type= x[10], photo = x[5], instock= x[7], new = x[8], price_check= x[9], product_link=x[11]))

    def calculate_savings(self, product):
        price = product.price[1:-3].replace(',', '')
        product.savings = int(product.msrp) - int(price)
        if product.savings < 0:
            product.savings = product.savings * -1
            product.savings = "$" + f"{product.savings}" + " OVER MSRP"
        else:
            product.savings = "$" + f"{product.savings}"   


    @property
    def read_products_from_db(self):
        prod_tuple = db.getRetailers_Products()
        products = [self.parse_sql_tuple(x) for x in prod_tuple]
        for x in products:
            self.calculate_savings(x)
        return products


    def filter_products(self, json=False, product_type=None, sources_to_exclude=None, price_ceiling=0, use_status=None, **kwargs):
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
        price_ceiling = int(price_ceiling)
        use_status = list_from(use_status) or []
        # List typecast since chain is consumed upon iteration
        exclude = list(chain(product_type, sources_to_exclude, use_status))
        
        def filter_price_ceiling(x):
            if price_ceiling == 0:
                return False
            return x > price_ceiling

        def value_matches_filter(x):
            if isinstance(x, float):
                return filter_price_ceiling(x)
            return x in exclude

        def desirable(product):
            """Takes a ScrapedProduct object and returns user-desirability boolean."""
            prod_chars = [getattr(product, x) for x in ["source", "price_n", "new", "product_type"]]
            exclusion_matches = [value_matches_filter(x) for x in prod_chars]
            return any(exclusion_matches)

        filtered = list(filter(lambda p: not desirable(p), all_products))
        if json:
            return [x.jsonify() for x in filtered]
        return filtered

interface = ProductDBInterface()

def unique_json_key(x):
    """Returns a unique JSON Key based on ScrapedProduct data. Takes a JSON blob/dict."""
    return f"{x['source'].lower()}_{x['name'].lower().replace(' ', '_')}"

@app.route("/resources/products", methods=["POST"])
@login_required
def search_products_api(**kwargs):
    """This endpoint makes it easier to test filtering.
       Leaving it in for now because we still need to implement
       product_type and that will need to be tested.
    """
    if request.method == 'POST':
        filters = request.json or {}
        return { unique_json_key(x): x for x in interface.filter_products(json=True, **filters)}

@app.route("/")
def home():
    return render_template('home.html')

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
                return redirect(url_for('listings'))
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
                return redirect(url_for('listings'))
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


@app.route("/listings", methods=("GET", "POST"))
@login_required
def listings():
    if request.method == "POST":
        data = request.form.to_dict()
        sources_to_exclude_keys = list(filter(lambda x: "sources_to_exclude" in x, list(data.keys())))
        data["sources_to_exclude"] = [data[x] for x in sources_to_exclude_keys]
        if not data['price_ceiling']:
            data['price_ceiling'] = 0
        return render_template('listings.html', items=interface.filter_products(**data))
    return render_template('listings.html', items=interface.filter_products())

if __name__ == '__main__':
    app.run()
