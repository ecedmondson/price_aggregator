from assets.sources.base_client import BaseMultiplesClient
from assets.scraped_product import ScrapedProduct

class Decluttr(BaseMultiplesClient):
    source = "Decluttr"
    use_status = "Used"

    def __init__(self, product_name, product_url, product_js, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.product_js = product_js
        super().__init__(**kwargs)

    def parse_web_element(self, element):
        def get_price(element):
            text = element.text
            text = text.replace("\n", "")
            start_ind = text.index("$")
            end_ind = text.index("REFURBISHED")
            return text[start_ind:end_ind]

        def get_photo(element):
            image = element.find_element_by_tag_name("img")
            return image.get_attribute("src")
        return ScrapedProduct(self.product_name, self.source, get_price(element), self.product_type, photo=get_photo(element), instock="In Stock", new=self.use_status)
    
    def scrape(self):
        product_elements = self.selenium.execute_script(self.product_js)
        return [self.parse_web_element(p) for p in product_elements]

