from assets.sources.base_client import BaseMultiplesClient
from assets.scraped_product import ScrapedProduct

JS_GET_COLOR_OPTIONS = """
r = document.getElementsByClassName("Row-uds8za-0 kPQaTV h-margin-v-tiny");
colors = r[0];
color_selenium = [];
for(var c = 0; c < colors.children.length; c++) {
    color_selenium.push(colors.children[c].children[0]);
}
return color_selenium;
"""

JS_GET_SIZE_OPTIONS = """
 r = document.getElementsByClassName("Row-uds8za-0 kPQaTV h-margin-v-tiny");  
sizes = r[1];
size_selenium = [];
for(var c = 0; c < sizes.children.length; c++) {
    size_selenium.push(sizes.children[c].children[0]);
}
return size_selenium;
"""

JS_GET_PRICE = """
v = document.getElementsByClassName("style__PriceFontSize-gob4i1-0");
e = Array.from(v).filter(o => o.innerHTML.includes("$"));
return e[0];
"""

JS_GET_PHOTO = """
return document.getElementsByClassName("slide--active")[0].getElementsByTagName('img')[0].attributes['src']
"""


class Target(BaseMultiplesClient):
    source = "Target"
    use_status = "New"

    def __init__(self, product_name, product_url, product_color, product_key, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.product_color = product_color
        self.product_key = product_key
        super().__init__(**kwargs)

    def get_config_value(self, element):
        cfg = element.get_attribute("aria-label")
        cfg = cfg.replace(" - checked", "")
        return cfg

    def get_retail_price(self, txt):
        txt = txt.replace("Retail price: ", "")
        return txt

    def parse_web_element(self, color, size, price, photo):
        photo = photo["value"]

        def stock(color, size):
            if "Out of stock" in color or "Out of stock" in size:
                return "Out of stock"
            return "In Stock"

        return ScrapedProduct(
            self.product_name,
            self.source,
            price,
            photo=photo,
            instock=stock(color, size),
            new=self.use_status,
        )

    def target_js_iteration(self):
        prices = []
        for color in self.selenium.execute_script(JS_GET_COLOR_OPTIONS):
            color.click()
        for size in self.selenium.execute_script(JS_GET_SIZE_OPTIONS):
            values = []
            values.append(self.get_config_value(color))
            values.append(self.get_config_value(size))
            size.click()
            values.append(
                self.get_retail_price(self.selenium.execute_script(JS_GET_PRICE).text)
            )
            values.append(self.selenium.execute_script(JS_GET_PHOTO))
            return values

    def scrape(self):
        return self.parse_web_element(*self.target_js_iteration())
