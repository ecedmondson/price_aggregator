from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient


class BandH(BaseClient):
    """A (hopefully) re-usable CompUSA web scraping client."""

    source = "B&H"
    use_status = "New"

    def __init__(self, product_name, product_url, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        self.backup_file = f"{self.product_name}/b_and_h.html"
        super().__init__(**kwargs)
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html.parser"),
        )

    def out_of_stock(self):
        return (
            "More on the Way"
            in self.soup.find(attrs={"data-selenium": "stockStatus"}).text
        )

    def get_price(self):
        f = open("b_and_h_macbook_air_2020_source.html", "w+")
        f.write(self.document)
        f.close()

        """Should only be called from inside get_product()"""
        return self.soup.find_all(attrs={"data-selenium": "pricingPrice"})[0].text

    def get_photo(self):
        """Should only be called from inside get_product()"""
        return self.soup.find_all(attrs={"data-selenium": "inlineMediaMainImage"})[
            0
        ].attrs["src"]
