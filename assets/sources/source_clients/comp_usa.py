from bs4 import BeautifulSoup
from bs4.element import Tag
from assets.sources.base_client import BaseClient


class CompUSA(BaseClient):
    """A (hopefully) re-usable CompUSA web scraping client."""

    source = "CompUSA"
    use_status = "New"

    def __init__(self, product_name, product_url):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        super().__init__()
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html.parser"),
        )

    def get_price(self):
        """Should only be called from inside get_product()"""
        return self.soup.find_all(attrs={"class": "deal-price"})[0].text

    def get_photo(self):
        """Should only be called form inside get_product()"""
        image_box = self.soup.find_all(attrs={"class": "product-image-slider"})[
            0
        ].contents
        image_div = list(filter(lambda d: isinstance(d, Tag), image_box))[0]
        return image_div.attrs["src"]
