from bs4 import BeautifulSoup
from bs4.element import Tag
from assets.sources.base_client import BaseClient

class CompUSA(BaseClient):
    source = "CompUSA"
    use_status = "New"
    def __init__(self, product_url):
        self.product_url = product_url
        # self.filename = filename
        super().__init__()
        self.document = self.get(self.product_url)
        self.soup = BeautifulSoup(self.document.text, features="html.parser")

    def get_price(self):
        return self.soup.find_all(attrs={"class": "deal-price"})[0].text

    def get_photo(self):
        image_box = self.soup.find_all(attrs={"class": "product-image-slider"})[0].contents
        image_div = list(filter(lambda d: isinstance(d, Tag), image_box))[0]
        return image_div.attrs['src']

c = CompUSA("https://www.compusa.com/deals/8638-BestBuy-14-HP-2-in-1-Touch-Screen-Chromebook-Intel-Core-i3-8130U-8GB-Memory-64GB-eMMC-Flash-Memory-Intel-UHD-Graphics-620-Chrome-OS-14-DA0012DX")
print(c.get_price())
print(c.get_photo())
