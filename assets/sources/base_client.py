from assets.config.config import cfg
from assets.scraped_product import ScrapedProduct
from assets.tools.tablewrite import HEADERS
from assets.tools.tablewrite import RSTWriter
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from fake_useragent import UserAgent
from jgt_common.http_helpers import is_status_code
from requests import get as rg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tableread import SimpleRSTReader
from time import sleep
from urllib3.exceptions import MaxRetryError
import os
import subprocess


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
            assert is_status_code("OK", r) is True
            return r
        except AssertionError:
            r = rg(url, headers=headers, **kwargs)
            if r.status_code >= 200 and r.status_code < 300:
                return r
            # If User Agent doesn't work, use backup
            f = open(f"{cfg.backup_path}/{self.backup_path}", "r")
            backup_text = f.read()
            f.close()
            return backup_text


results = dict()


def cache(func):
    def wrapper(*args, **kwargs):
        if kwargs["cache_id"] in results:
            return results[kwargs["cache_id"]]
        result = func(*args)
        results[kwargs["cache_id"]] = result
        return result

    return wrapper


# Selenium needed to be cached because
# the web scraping clients only needed one
# selenium instance to share among the
# subclasses, instead of multiple instances
# one for each subclass. Having multiple
# instances caused too many chrome instances
# running on flip.
@cache
def get_selenium_webdriver(cache_id=None):
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=New User Agent")
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(chrome_options=chrome_options)


@cache
def killed(cache_id=None):
    return True


@cache
def run_finally_block(cache_id=None):
    return True


class BaseSeleniumClient:
    def __init__(self):
        # google-chrome is installed on flip redhat osu servers
        # if you want to use something else locally, you will need
        # to configure this yourself
        chrome_options = Options()
        chrome_options.add_argument("--user-agent=New User Agent")
        chrome_options.add_argument("--headless")
        self.selenium = get_selenium_webdriver(
            cache_id="base_client_selenium_webdriver"
        )
        self.pid_proc = self.selenium.service.process.pid

    def __del__(self):
        try:
            if "selenium_is_dead" not in results:
                print("Trying to close Selenium Google Chrome Instance.")
                self.selenium.close()
                print(f"Trying to kill chromedriver pid at {self.pid_proc}.")
                kill = subprocess.Popen(
                    f"kill {self.pid_proc}", shell=True, stdout=subprocess.PIPE
                ).stdout
                killed(cache_id="selenium_is_dead")
        except (ImportError, MaxRetryError) as e:
            print(
                f"SELENIUM SHUTDOWN ERROR: highly recommended to manually pgrep for {self.pid_proc}."
            )
            print(f"Original Error:\n\t {type(e)}: {e}.")
        finally:
            if "selenium_finally_block" not in results:
                run_finally_block(cache_id="selenium_finally_block")
                check = subprocess.Popen(
                    "pgrep -lf chrome", shell=True, stdout=subprocess.PIPE
                ).stdout
                grep = check.read().decode("utf-8")
                if str(self.pid_proc) in grep:
                    print(
                        f"{self.pid_proc} found running after trying to kill Selenium Chrome & Chromedriver."
                    )
                    print("You might want to manually check file handles.")

    def dynamic_get(self, url):
        self.selenium.get(url)
        return self.selenium.page_source

    def navigate_to_page(self, url):
        """Navigates to page only. Does not return page source."""
        self.selenium.get(url)

class BaseCachingClient:
    # We can change this implementation, but
    # some form of caching needs to take place
    # to avoid rate-limiting. Another option
    # may be writing to a DB, but this is a
    # stop gap for the meantime.

    def filepath(self, filename):
        return f"{cfg.cache_path}{filename}.rst".replace("-", "_").replace(" ", "_")

    def any_cached_data(self, filename):
        return os.path.exists(self.filepath(filename))

    def data_within_ttl(self, filename, tablename="Product"):
        reader = SimpleRSTReader(self.filepath(filename))
        table = reader["Default"]
        ttl = table.get_fields("ttl")
        cache_time = table.get_fields("timestamp")
        try:
            if datetime.now() > (parse(cache_time[0]) + timedelta(hours=int(ttl[0]))):
                return False
            return True
        except ParserError:
            return False

    def get_cached_data(self, filename):
        reader = SimpleRSTReader(self.filepath(filename))
        table = reader["Default"]
        return (
            table.get_fields("price")[0],
            table.get_fields("photo")[0],
            table.get_fields("timestamp")[0],
        )

    def cache_data(self, filename, products):
        client = RSTWriter()
        grid = [HEADERS]
        [
            grid.append([p.name, p.price, p.photo, str(datetime.now()), "24"])
            for p in products
        ]
        client.write_table_to_file(self.filepath(filename), grid)


class BaseContainer:
    """Container for self.document and self.soup."""

    def __init__(self, **kwargs):
        self.add(**kwargs)

    def add(self, **kwargs):
        self.__dict__.update(kwargs)


class BaseClient(BaseRequestsClient, BaseSeleniumClient, BaseCachingClient):
    """BaseClient which all products inherit from"""

    def __init__(self, product_type=None, msrp=None):
        super(BaseRequestsClient, self).__init__()
        super(BaseSeleniumClient, self).__init__()
        super(BaseCachingClient, self).__init__()
        self.scraper = BaseContainer()
        self.product_type=product_type
        self.msrp = msrp

    def __getattr__(self, item):
        # Overwriting __getattr__ allows us to set
        # self.document and self.soup on the product
        # objects as lambdas, meaning that they exist
        # for our use whenever we need them but aren't
        # called at module load. The benefit of this is
        # that we are less likely to be rate-limited
        # by making multiple automated requests.
        lambdas = ["soup", "document"]
        if item in lambdas:
            item = self.scraper.__getattribute__(item)
            return item()
        return super().__getattribute__(item)

    def data_cached_and_available(self):
        """Returns True is there is data cached and it is within the timeout"""
        return self.any_cached_data(self.filename) and self.data_within_ttl(
            self.filename
        )

    def get_last_known_valid_cache(self, backup):
        f = open(f"{cfg.backup_path}/{backup}", "r")
        backup_text = f.read()
        f.close()
        self.scraper.document = lambda: backup_text
        self.scraper.soup = lambda: BeautifulSoup(backup_text, features="html5lib")
        return self.get_price(), self.get_photo()

    def scraped_or_cached_product(self):
        if self.data_cached_and_available():
            price, photo, timestamp = self.get_cached_data(self.filename)
            return ScrapedProduct(
                self.msrp,
                self.product_name,
                self.source,
                price,
                self.product_type,
                photo=photo,
                new=self.use_status,
                price_check=parse(timestamp),
                product_link=self.product_url,
            )
        product = ScrapedProduct(
            self.msrp,
            self.product_name,
            self.source,
            self.get_price(),
            self.product_type,
            photo=self.get_photo(),
            new=self.use_status,
            product_link=self.product_url,
        )
        self.cache_data(self.filename, [product])
        return product

    def get_product(self):
        if not self.out_of_stock():
            return self.scraped_or_cached_product()
        price, photo = self.get_last_known_valid_cache(self.backup_file)
        return ScrapedProduct(
            self.msrp,
            self.product_name,
            self.source,
            price,
            self.product_type,
            photo=photo,
            new=self.use_status,
            instock="Out of Stock (Last Known Price Listed)",
            product_link=self.product_url,
        )

class BaseMultiplesClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product(self):
        self.navigate_to_page(self.product_url)
        return self.scrape()
    
