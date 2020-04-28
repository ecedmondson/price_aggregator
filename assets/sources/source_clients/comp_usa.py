from bs4 import BeautifulSoup
from bs4.element import Tag
from assets.sources.base_client import BaseClient

class CompUSA(BaseClient):
    source = "CompUSA"
    use_status = "New"
    def __init__(self, product_name, product_url):
        self.product_name = product_name
        self.product_url = product_url
        # self.filename = filename
        super().__init__()
        self.scraper.add(
            document=lambda: self.get(self.product_url),
            soup=lambda: BeautifulSoup(self.document.text, features="html.parser")
        )

    def get_price(self):
        """Should only be called from inside get_product()"""
        return self.soup.find_all(attrs={"class": "deal-price"})[0].text

    def get_photo(self):
        """Should only be called form inside get_product()"""
        image_box = self.soup.find_all(attrs={"class": "product-image-slider"})[0].contents
        image_div = list(filter(lambda d: isinstance(d, Tag), image_box))[0]
        return image_div.attrs['src']

c = CompUSA("HP-2-in-1 Chromebook", "https://www.compusa.com/deals/8638-BestBuy-14-HP-2-in-1-Touch-Screen-Chromebook-Intel-Core-i3-8130U-8GB-Memory-64GB-eMMC-Flash-Memory-Intel-UHD-Graphics-620-Chrome-OS-14-DA0012DX")
print(c.get_product())
print(c.get_price())
