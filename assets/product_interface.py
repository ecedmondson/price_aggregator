from assets.products.product_clients.chromebook import HPTouchScreenChromebook
# from assets.products.product_clients.macbookair import MacBookAir2020
from assets.sources.base_client import BaseContainer
from itertools import chain
from time import time

def list_from(item):
    if not item:
        return []
    if isinstance(item, (str, dict)) or not is_iterable(
        item
    ):
        return [item]
    return list(item)

class ProductInterface:
    """Interface object so that the UI can easily obtain filtered products."""
    def __init__(self):
        self.container = BaseContainer()
        self.container.add(
            chrome=HPTouchScreenChromebook,
        )

        self.all_products = [self.chrome]
    
    def __getattr__(self, item):
        if item not in ['container', 'all_products']:
            item = self.container.__getattribute__(item)
            print(item)
            return item()
        return super().__getattribute__(item)
            
    def scrape(self, cache_id="interface_scrape"):
        print("DEBUG: retrieval of products...")
        start = time()
        p = list(chain.from_iterable([x.products for x in self.all_products]))
        print(f"Retrieval took {time() - start} seconds.")
        return p

    def get_products_by_filters(self, json=True, product_type=None, sources_to_exclude=None, price_ceiling=None, use_status=None):
        """Pass filters as kwargs
        
        Filter options:
            - product_type (str): 'computer' or 'tablet'
            - sources_to_exclude (str): a retailer, i.e. 'amazon'
            - price_ceiling (int): highest price
            - use_status (str): use status, i.e. new or used
        """

        all_products = self.scrape()
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
        if json:
            return [x.jsonify() for x in filtered]
        return filtered

p = ProductInterface()
print(p.scrape())
print(p.get_products_by_filters())
