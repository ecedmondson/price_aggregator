from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient


class Walmart(BaseClient):
    """A (hopefully) reusable Walmart scraping client."""

    source = "Walmart"
    use_status = "New"

    def __init__(self, product_name, product_url, product_img_alt, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.product_img_alt = product_img_alt
        self.filename = f"{self.source.lower()}_{self.product_name}"
        self.backup_file=f"{self.product_name}/{self.source.lower().replace(' ', '_')}.html"
        super().__init__(**kwargs)
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html.parser"),
        )

    def out_of_stock(self):
        return "Out of stock" in self.soup.find(attrs={"class": "product-atf"}).text

    def get_price(self):
        return f"${self.soup.find(id='price').text.split('$')[-1]}"

    def get_photo(self):
        imgs = self.soup.find_all("img")
        imgs = list(filter(lambda e: "alt" in e.attrs.keys(), imgs))
        imgs = list(filter(lambda e: self.product_img_alt in e.attrs["alt"], imgs))
        return imgs[0].attrs["src"]

class WalmartRefurbished(Walmart):
    use_status = "Used"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

