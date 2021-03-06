from assets.sources.base_client import BaseClient
import bs4


class BestBuy(BaseClient):
    source = "Best Buy"
    use_status = "New"

    def __init__(self, product_name, product_url, **kwargs):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        self.backup_file=f"{self.product_name}/{self.source.lower().replace(' ', '_')}.html"
        super().__init__(**kwargs)
        self.scraper.add(
            document=lambda: self.dynamic_get(self.product_url),
            soup=lambda: bs4.BeautifulSoup(self.document, features="html.parser"),
        )

    def out_of_stock(self):
        add_to_cart_button = self.soup.find(
            attrs={"class": "fulfillment-add-to-cart-button"}
        )
        try:
            return "Sold Out" in add_to_cart_button.text
        except AttributeError:
            return True

    def get_price(self):
        try:
            price = self.soup.find(attrs={"class": "price-box"}).find(attrs={"class": "priceView-customer-price"})
            return price.text.split(" ")[-1]
        except Exception:
            price_boxes = self.soup.find_all(attrs={"class": "priceView-layout-large"})
            correct_box = [
                x
                for box in price_boxes
                for x in box.contents
                if "Price Match Guarantee" in x.text
            ]
            text_content = correct_box[0].text
            text_content = text_content.replace("Price Match Guarantee", "")
            return text_content[: text_content.find("Your price")]

    def get_photo(self):
        return self.soup.find(attrs={"class": "primary-image"}).attrs["src"]
