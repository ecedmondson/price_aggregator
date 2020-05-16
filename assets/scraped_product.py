from assets.config.config import cfg
from datetime import datetime
import json

class ScrapedProduct:
    """Object to represent a scraped Product.
    This class is a container for the common attributes pertinent
    to any product that is scraped by the Price Aggregator. The
    data is organized into this object as an easy to access those
    shared attributes.
    """

    def __init__(
        self, product_type, name, source, price, photo=None, instock=None, new=None, price_check=None
    ):
        self.output = "Scraped Product debug info: "
        self.product_type = product_type or 'Electronics'
        self.name = " ".join([x.upper() for x in name.split("_")[1:]])
        self.source = source
        self.price = price
        self.price_n = float(price[1:].replace(",",""))
        self.photo = photo or cfg.product_photo_default
        self.instock = instock or cfg.stock_default
        self.new = new or cfg.use_status
        self.price_check = price_check or datetime.now()

    def __str__(self):
        return "\n".join(
            [
                f"\t{k}: {v}" if k != "output" else f"{v}"
                for k, v in self.__dict__.items()
            ]
        )

    def jsonify(self):
        p = self.__dict__.copy()
        p.pop('output')
        p['price_check'] = p['price_check'].isoformat()
        return p

