from bs4 import BeautifulSoup
from assets.sources.base_client import BaseClient

class Amazon(BaseClient):
    source = "Amazon"
    use_status = "New"
    def __init__(self, product_url):
        self.product_url = product_url
        super().__init__()
        self.document = self.get(self.product_url)
        # self.document = self.dynamic_get(self.product_url)
        # self.product_unavailable = isinstance(self.document, str)
        self.soup = BeautifulSoup(self.document.text, features="html5lib")

    def get_price(self):
        # price_inside_buybox only seems to work with New products
        f = open("test.txt", 'w+')
        f.write(self.document.text)
        f.close()
        return self.soup.find(id="price_inside_buybox")

    def get_photo(self):
        # parent is id="imgTagWrapperId
        return self.soup.find(id="landingImage").attrs['src']

a = Amazon("https://www.amazon.com/HP-15-inch-i7-8750H-Processor-15-dc0045nr/dp/B07H9XPF1S?ref_=ast_sto_dp")
print(a.get_price())
print(a.get_photo())
