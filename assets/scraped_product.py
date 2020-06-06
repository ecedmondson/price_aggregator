from assets.config.config import cfg
from datetime import datetime

 
MANUFACTURERS = {
    "14DA0012DX_hp_chromebook": "HP",
    "MWTL2LL-A_macbook_air": "Apple",
    "MY252LL-A_ipad_pro_11_inch": "Apple",
    "MVFH2LL-A_macbook_air_2019": "Apple",
    "skytech_gaming_ST_Arch3.0_0056_NE": "Skytech",
    "VDV-00001_surface": "Microsoft"
}

def make_readable_name(name):
    if "GAMING" not in name.upper():
        return " ".join([x.upper() for x in name.split("_")[1:]])
    return "SKYTECH ARCHANGEL"

def get_manufacturer(name):
    return MANUFACTURERS[name]

class ScrapedProduct:
    """Object to represent a scraped Product.
    This class is a container for the common attributes pertinent
    to any product that is scraped by the Price Aggregator. The
    data is organized into this object as an easy to access those
    shared attributes.
    """

    def __init__(
        self, msrp, name, source, price, product_type, photo=None, instock=None, new=None, price_check=None, product_link=None
    ):
        self.output = "Scraped Product debug info: "
        self.name = name
        self.manufacturer = get_manufacturer(self.name)
        self.readable_name = make_readable_name(self.name)
        self.source = source
        self.price = price
        self.price_n = float(price.replace("$", "").replace(",", ""))
        self.photo = photo or cfg.product_photo_default
        self.instock = instock or cfg.stock_default
        self.new = new or cfg.use_status
        self.price_check = price_check or datetime.now()
        self.product_type = product_type
        self.msrp = msrp
        self.product_link = product_link 
    def __str__(self):
        return "\n".join(
            [
                f"\t{k}: {v}" if k != "output" else f"{v}"
                for k, v in self.__dict__.items()
            ]
        )

    def jsonify(self):
        p = self.__dict__.copy()
        del p['output']
        return p
