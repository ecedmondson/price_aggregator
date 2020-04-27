from bs4 import BeautifulSoup
from requests import get

class Walmart():
    def __init__(self, product_url, product_img_alt):
        self.product_url = product_url
        self.product_img_alt = product_img_alt
        self.document = get(product_url)
        self.soup = BeautifulSoup(self.document.text, features="html.parser")

    def get_price(self):
        return f"${self.soup.find(id='price').text.split('$')[-1]}"

    def get_photo(self):
        imgs = self.soup.find_all("img")
        imgs = list(filter(lambda e: "aria-hidden" not in e.attrs, imgs))
        imgs = list(filter(lambda e: bool(e.attrs['src']), imgs))
        imgs = list(filter(lambda e: 'alt' in e.attrs, imgs))
        imgs = list(filter(lambda e: self.product_img_alt in e.attrs['alt'], imgs))
        return imgs[0].attrs['src']

w = Walmart("https://www.walmart.com/ip/HP-2-in-1-14-Full-HD-Touchscreen-Chromebook-x360-Core-i3-8130U-8GB-RAM-64GB-eMMC/814497767", "HP 2-in-1 14")
a = Walmart("https://www.walmart.com/ip/Acer-Chromebook-715-8th-Gen-Intel-Core-i3-8130U-15-6-Full-HD-Touchscreen-4GB-DDR4-128GB-eMMC-CB715-1WT-39HZ/435795966?findingMethod=wpa", "Acer Chromebook 715")
