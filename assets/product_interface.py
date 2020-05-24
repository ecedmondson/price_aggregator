from itertools import chain
from app import db

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


    def get_products_by_filters(self, json=True, product_type=None, sources_to_exclude=None, price_ceiling=None, use_status=None):
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
        if json:
            return [x.jsonify() for x in filtered]
        return filtered

p = ProductInterface()
print(p.read_products_from_db)
# print(p.get_products_by_filters())
