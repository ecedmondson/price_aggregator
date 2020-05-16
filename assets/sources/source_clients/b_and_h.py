from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient


class BandH(BaseClient):
    """A (hopefully) re-usable CompUSA web scraping client."""

    source = "B&H"
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
        return self.soup.find_all(attrs={"data-selenium": "pricingPrice"})[0].text
	
    def get_photo(self):
        """Should only be called from inside get_product()"""
        return self.soup.find_all(attrs={"data-selenium": "inlineMediaMainImage"})[0].attrs['src']

