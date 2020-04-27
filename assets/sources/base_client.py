from requests import get as rg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jgt_common.http_helpers import is_status_code
from fake_useragent import UserAgent


class BaseRequestsClient:
    def get(self, url, **kwargs):
        # headers = {
        #    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
        # }
        ua = UserAgent()
        hdr = {
            "User-Agent": ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        try:
            r = rg(url, **kwargs)
            print(r)
            assert is_status_code("OK", r) is True
            return r
        except AssertionError:
            r = rg(url, headers=hdr, **kwargs)
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
        self.selenium = webdriver.Chrome(chrome_options=chrome_options)

    def __del__(self):
        self.selenium.quit()

    def dynamic_get(self, url):
        self.selenium.get(url)
        return self.selenium.page_source


class BaseClient(BaseRequestsClient, BaseSeleniumClient):
    """BaseClient which all products inherit from"""

    def __init__(self):
        super(BaseRequestsClient, self).__init__()
        super(BaseSeleniumClient, self).__init__()
