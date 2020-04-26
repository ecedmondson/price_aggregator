from bs4 import BeautifulSoup
from requests import get
from itertools import chain
from builtins import any

# def cache_scraped_products(func):
#    cache = {}
#    def wrapper(*args, **kwargs):
        
class Chromebook():
    subclasses = set()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "sub_name" in cls.__dict__:
            cls.subclasses.add(cls)

    def filter_products(self, sources_to_exclude=None, price_ceiling=None, use_status=None):
        sources_to_exclude = sources_to_exclude or []
        price_ceiling = price_ceiling or []
        use_status = use_status or []
        exclude = chain(sources_to_exclude, use_status)
        def desirable(product):
            """Takes a ScrapedProduct object and returns user-desirability boolean."""
            product_characteristics = [getattr(product, x) for x in ["source", "price_int", "use"]]
            matches = [x in exclude if not isinstance(x, int) else x < price_ceiling for x in exclude]               return any(matches)
        return list(filter(lambda p: not desirable(p), self.products))
    
    def get_all_products():
        """List of ScrapedProduct objects."""             
        return [p for client in self.clients for p in client.scrape_products()]

class 14DA0012DX(Chromebook):
    model = "14-DA0012DX"
    sub_name = "Chromebook 14-DA0012DX"
    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients():
        return [BestBuy(), CompUSA(), Newegg(), Walmart(), Amazon()]
         
