from assets.sources.base_client import BaseClient
import bs4

def get_docs(product_name):
    if 'chromebook' in product_name:
        f = open('assets/data/best_buy_chromebook.txt', 'r')
        data = f.read()
        f.close()
        return data

class BestBuy(BaseClient):
    source = "Best Buy"
    use_status = "New"

    def __init__(self, product_name, product_url):
        self.product_name = product_name
        self.product_url = product_url
        self.filename = f"{self.source.lower()}_{self.product_name}"
        super().__init__()
        # self.document = get_docs(self.product_name)
        self.scraper.add(
            document=lambda: self.dynamic_get(product_url),
            soup=lambda: bs4.BeautifulSoup(self.document, features="html.parser"),
        )

    def out_of_stock(self):
        add_to_cart_button = self.soup.find(
            attrs={"class": "fulfillment-add-to-cart-button"}
        )
        return "Sold Out" in add_to_cart_button.text

    def get_price(self):
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

#b = BestBuy("blah_blah", "https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-core-i3-8gb-memory-64gb-emmc-flash-memory-white/6365772.p?skuId=6365772")
# b = BestBuy("bt", "https://twitter.com/home")
# print(b.get_product())
