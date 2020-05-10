from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient


class Amazon(BaseClient):
    """A (hopefully) re-usable Amazon web scraping client."""

    source = "Amazon"
    use_status = "New"

    def __init__(self, product_name, product_url):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        super().__init__()
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html5lib"),
        )

    def get_price(self):
        # price_inside_buybox only seems to work with New products
        return self.soup.find(id="price_inside_buybox").text.strip()

    def get_photo(self):
        # parent is id="imgTagWrapperId
        return self.soup.find(id="landingImage").attrs["src"]

class AmazonUsed(Amazon):
    """ A (hopefully) re-usable Amazon web-scraping client for used content."""
    source = "Amazon"
    use_status = "Used"

    def get_price(self):
        # usedBuySection only works with New products
        return self.soup.find(id="usedBuySection").text.replace("Buy used:", "").strip()

    def get_photo(self):
        attrs = self.soup.find(id="landingImage").attrs
        if "data-old-hires" not in attrs.keys():
            return None
        return attrs["data-old-hires"]

