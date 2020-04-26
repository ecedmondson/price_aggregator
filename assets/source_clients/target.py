from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests import get
import os

# Move to assets/selenium_js
JS_GET_PRICE = """
v = document.getElementsByClassName("h-text-sm h-text-grayDark");
e = Array.from(v).filter(o => o.innerHTML.includes("Retail price: "));
return e[0];
"""

class Target():
    def __init__(self, product_url):
        self.product_url = product_url
        self.selenium = self.get_driver()
        self.page = self.selenium.get(self.product_url)

    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=chrome_options)


t = Target("https://www.target.com/p/apple-iphone-11/-/A-78052843?lnk=iphone11")
p = t.execute_script(JS_GET_PRICE)
print(p)

