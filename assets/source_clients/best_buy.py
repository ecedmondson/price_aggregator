import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BestBuy():
    source = "Best Buy"
    status = "New"
    def __init__(self, product_url, best_buy_sku):
        self.product_url = product_url
        self.best_buy_sku = best_buy_sku
        self.selenium = self.get_driver()
        self.document = self.get_html()
        self.soup = bs4.BeautifulSoup(self.document, features="html.parser")

    def get_html(self):
        try:
            f = open(f'tmp/best_buy/{self.best_buy_sku}.txt')
            lines = f.read()
            f.close()
            return lines
        except FileNotFoundError:
            f = open(f'tmp/best_buy/{self.best_buy_sku}.txt', 'w+')
            f.write(self.selenium.page_source)
            f.close()
            # need to write some sort of TTL caching
            print(type(self.selenium.page_source))
            return self.selenium.page_source

    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        w = webdriver.Chrome(chrome_options=chrome_options)
        w.get(self.product_url)
        return w

    def get_price(self):
        SELENIUM_JS_PRICE = (
            f"""
            box = document.getElementById('{self.price_box_id}');
            return box.getElementsByClassName("priceView-customer-price")[0].textContent
            """
        )
        print(SELENIUM_JS_PRICE)
        return self.selenium.execute_script(SELENIUM_JS_PRICE)[1:7]

    def get_price_soup(self):
        price_boxes = self.soup.find_all(attrs={"class":"priceView-layout-large"})
        correct_box = [x for box in price_boxes for x in box.contents if "Price Match Guarantee" in x.text]
        text_content = correct_box[0].text
        text_content = text_content.replace("Price Match Guarantee", "<").replace("Your price", "<")
        text_content = text_content.split("<")
        return text_content[1]
    
    def get_photo(self):
        return self.soup.find(attrs={"class": "primary-image"}).attrs['src']

url = "https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-core-i3-8gb-memory-64gb-emmc-flash-memory-white/6365772.p?skuId=6365772"

iother = "https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-celeron-4gb-memory-32gb-emmc-flash-memory-ceramic-white/6367729.p?skuId=6367729"

