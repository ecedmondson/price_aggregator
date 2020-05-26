from itertools import chain
from builtins import any


class BaseProduct:
    """Do not instantiate this class. This is meant to provide general use fuctionality for all products."""

    subclasses = set()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "sub_name" in cls.__dict__:
            cls.subclasses.add(cls)

    def get_all_products(self):
        """List of ScrapedProduct objects."""
        return [client.get_product() for client in self.clients]

