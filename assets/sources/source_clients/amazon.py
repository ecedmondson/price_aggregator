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
        self.backup_file = f"{self.product_name}/{self.source.lower()}.html"
        super().__init__()
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html5lib"),
        )

    def out_of_stock(self):
        return "Temporarily out of stock." in self.document.text

    def get_price(self):
        # price_inside_buybox only seems to work with New products
        try:
            return self.soup.find(id="price_inside_buybox").text.strip()
        except AttributeError:
            r = self.soup.find(id="priceblock_ourprice_row")
            if r:
               r = r.text
               s_ind = r.find('$')
               e_ind = r.find('&')
               return r[s_ind:e_ind].strip()
            return None

    def get_photo(self):
        image = self.soup.find(id="landingImage")
        try:
            return image.attrs["data-old-hires"]
        except (AttributeError, ValueError):
            return image.attrs['src']

class AmazonUsed(Amazon):
    """ A (hopefully) re-usable Amazon web-scraping client for used content."""

    source = "Amazon"
    use_status = "Used"

    def get_price(self):
        # usedBuySection only works with New products
        if not super().get_price():
            return self.soup.find(id="usedBuySection").text.replace("Buy used:", "").strip()

