from bs4 import BeautifulSoup
from bs4.element import Tag
from assets.sources.base_client import BaseClient


class Skytech(BaseClient):
    """A (hopefully) re-usable CompUSA web scraping client."""

    source = "Skytech"
    use_status = "New"

    def __init__(self, product_name, product_url, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        self.backup_file = f"{self.product_name}/skytech.html"
        super().__init__(**kwargs)
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html.parser"),
        )

    def out_of_stock(self):
        return bool(self.document.text)

    def get_price(self):
        """Should only be called from inside get_product()"""
        return f'${self.soup.find(attrs={"class": "woocommerce-Price-amount"}).text}'

    def get_photo(self):
        """Should only be called from inside get_product()"""
        photo_box = self.soup.find(attrs={"class": "woocommerce-product-gallery__wrapper"}).contents
        return list(filter(lambda x: isinstance(x, Tag), photo_box))[0].contents[0].contents[0].attrs["src"]

