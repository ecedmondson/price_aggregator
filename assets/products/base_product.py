from itertools import chain
from builtins import any

class BaseProduct():
    """Do not instantiate this class. This is meant to provide general use fuctionality for all products."""
    subclasses = set()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "sub_name" in cls.__dict__:
            cls.subclasses.add(cls)

    def get_all_products(self):
        """List of ScrapedProduct objects."""             
        return [client.get_product() for client in self.clients]

    def filter_products(self, sources_to_exclude=None, price_ceiling=None, use_status=None):
        all_product = self.get_all_products()
        sources_to_exclude = sources_to_exclude or []
        price_ceiling = price_ceiling or 0
        use_status = use_status or []
        # List typecast since chain is consumed upon iteration
        exclude = list(chain(sources_to_exclude, use_status))
        def desirable(product):
            """Takes a ScrapedProduct object and returns user-desirability boolean."""
            prod_chars = [getattr(product, x) for x in ["source", "price_int", "use"]]
            exclusion_matches = [x in exclude if not isinstance(x, int) else x < price_ceiling for x in prod_chars]
            return any(exclusion_matches)
        return list(filter(lambda p: not desirable(p), all_products))

