from assets.configs.config import cfg
from datetime import date

class ScrapedProduct():
    """Object to represent a scraped Product.

    This class is a container for the common attributes pertinent
    to any product that is scraped by the Price Aggregator. The
    data is organized into this object as an easy to access those
    shared attributes.
    """
    def __init__(self, name, source, price, photo=None, instock=None, new=None, price_check=None):
        self.name = name
        self.source = source
        self.price = price
        self.photo = photo or cfg.product_photo_default
        self.instock = instock or cfg.stock_default
        self.new = new or cfg.use_status
        self.price_check = price_check or date.today()
