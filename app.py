from flask import Flask, render_template
from database.db import Database
app = Flask(__name__)

items = [
    {
        'name': 'best buy_14DA0012DX_hp_chromebook',
        'source': 'Best Buy',
        'price': '$599.00',
        'photo': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6365/6365772_sd.jpg;maxHeight=640;maxWidth=550',
        'instock': 'Likely In Stock, Check Retailer',
        'new': 'New',
        'price_check': '2020-04-30 18:38:19.752171',
    },
    {
        'name': 'best buy_14DA0012DX_hp_chromebook',
        'source': 'Best Buy',
        'price': '$599.00',
        'photo': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6365/6365772_sd.jpg;maxHeight=640;maxWidth=550',
        'instock': 'Likely In Stock, Check Retailer',
        'new': 'New',
        'price_check': '2020-04-30 18:38:19.752171',
    },
]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/listings")
def listings():
    return render_template('listings.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
