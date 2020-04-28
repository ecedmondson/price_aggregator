from requests import get as rg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jgt_common.http_helpers import is_status_code
from fake_useragent import UserAgent
from assets.scraped_product import ScrapedProduct
from assets.config.config import cfg
from assets.tools.tablewrite import HEADERS
from assets.tools.tablewrite import RSTWriter
from tableread import SimpleRSTReader
from datetime import datetime
from dateutil.parser import parse
from datetime import timedelta
import os


class BaseRequestsClient:
    def get(self, url, **kwargs):
        # Some websites get cranky and want better UA info.
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        try:
            r = rg(url, **kwargs)
            print(r.text)
            print(r)
            assert is_status_code("OK", r) is True
            return r
        except AssertionError:
            r = rg(url, headers=headers, **kwargs)
            if r.status_code >= 200 and r.status_code < 300:
                return r
            return False


class BaseSeleniumClient:
    def __init__(self):
        # google-chrome is installed on flip redhat osu servers
        # if you want to use something else locally, you will need
        # to configure this yourself
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # self.selenium = webdriver.Chrome(chrome_options=chrome_options)

    def __del__(self):
        self.selenium.quit()

    def dynamic_get(self, url):
        self.selenium.get(url)
        return self.selenium.page_source

class BaseCachingClient():
    # We can change this implementation, but
    # some form of caching needs to take place
    # to avoid rate-limiting.

    def filepath(self, filename):
        return f"{cfg.cache_path}{filename}.rst".replace("-", "_").replace(" ", "_")

    def any_cached_data(self, filename):
        return os.path.exists(self.filepath(filename))

    def data_within_ttl(self, filename, tablename="Product"):
        reader = SimpleRSTReader(self.filepath(filename))
        table = reader['Default']
        ttl = table.get_fields("ttl")
        cache_time = table.get_fields("timestamp")
        if datetime.now() > (parse(cache_time[0]) + timedelta(hours=int(ttl[0]))):
            print(f"Data not within ttl")
            return False
        return True

    def get_cached_data(self, filename):
        reader = SimpleRSTReader(self.filepath(filename))
        table = reader["Default"]
        return (table.get_fields("price")[0], table.get_fields("photo")[0], table.get_fields("timestamp")[0])

    def cache_data(self, filename, products):
        client = RSTWriter()
        grid = [HEADERS]
        [grid.append([p.name, p.price, p.photo, str(datetime.now()), "24"]) for p in products]
        client.write_table_to_file(self.filepath(filename), grid)

class BaseContainer():
    def __init__(self, **kwargs):
        self.add(**kwargs)

    def add(self, **kwargs):
        self.__dict__.update(kwargs)

class BaseClient(BaseRequestsClient, BaseSeleniumClient, BaseCachingClient):
    """BaseClient which all products inherit from"""

    def __init__(self):
        super(BaseRequestsClient, self).__init__()
        super(BaseSeleniumClient, self).__init__()
        super(BaseCachingClient, self).__init__()
        self.scraper = BaseContainer()

    def __getattr__(self, item):
        # Might need to write a container for this
        lambdas = ["soup", "document"]
        if item in lambdas:
            item = self.scraper.__getattribute__(item)
            return item()
        return super().__getattribute__(item)

    @staticmethod
    def price(func):
        def wrapper(self, *args):
            if self.any_cached_data(self.filename) and self.data_within_ttl(self.filename):
                return self.get_cached_data(self.filename)[0]
            return func(args)
        return wrapper

    @staticmethod
    def photo(func):
        def wrapper(self, *args):
            if self.any_cached_data(self.filename) and self.data_within_ttl(self.filename):
                return self.get_cached_data(self.filename)[1]
            return func(args)
        return wrapper

    def get_product(self):
        if self.any_cached_data(self.product_name) and self.data_within_ttl(self.product_name):
            price, photo, timestamp = self.get_cached_data(self.product_name)
            print("WE DID IT!")
            return ScrapedProduct(self.product_name, self.source, price, photo=photo, new=self.use_status, price_check=parse(timestamp))
        product = ScrapedProduct(self.product_name, self.source, self.get_price(), photo=self.get_photo(), new=self.use_status)
        self.cache_data(self.product_name, [product])
        return product