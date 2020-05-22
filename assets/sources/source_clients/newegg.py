from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient
from bs4.element import Tag


class NewEgg(BaseClient):
    """A (hopefully) re-usable CompUSA web scraping client."""

    source = "NewEgg"
    use_status = "New"

    def __init__(self, product_name, product_url):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        super().__init__()
        self.scraper.add(
            document=lambda: self.dynamic_get(self.product_url),
            soup=lambda: BeautifulSoup(self.document, features="html.parser"),
        )

    def out_of_stock(self):
        return "OUT OF STOCK" in self.soup.find(attrs={"id": "landingpage-stock"}).text

    def get_price(self):
        """Should only be called from inside get_product()"""
        f = open("newegg_macbook_air_2020_source.html", "w+")
        f.write(self.document)
        f.close()

        text = self.soup.find_all(attrs={"id": "landingpage-price"})[0].text
        ind = text.find("$")
        return text[ind:]

    def get_photo(self):
        """Should only be called form inside get_product()"""
        elements = self.soup.find_all(attrs={"class": "mainSlide"})[0].contents
        img = list(filter(lambda e: isinstance(e, Tag), elements))
        return img[0].attrs["src"]
