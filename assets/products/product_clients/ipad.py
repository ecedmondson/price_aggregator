from assets.products.base_product import BaseProduct
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.target import Target
from assets.sources.source_clients.b_and_h import BandH
from assets.sources.source_clients.walmart import Walmart

# The iPad Pro 11 Inch has multiple configurations, all of which might have a different MSRP. As a result of this,
# I have intentionally only scraped the 2020 Silver 128 GB with Wifi in this object.
# MSRP Source of Truth for this product is the Apple Manufacturer: https://www.walmart.com/ip/Apple-11-inch-iPad-Pro-2020-Wi-Fi-128GB-Silver/700142742
# on 5/27/2020 this was listed as $799

class iPadPro11InchSilver128GB2020(BaseProduct):
    target_keys = ("Silver", "128GB")
    product_type = "Tablet"
    msrp="799"
    best_buy = "https://www.bestbuy.com/site/apple-11-inch-ipad-pro-latest-model-with-wi-fi-128gb-silver/3756005.p?skuId=3756005"
    b_and_h = "https://www.bhphotovideo.com/c/product/1553825-REG/apple_my252ll_a_11_ipad_pro_early.html"
    target = "https://www.target.com/p/apple-ipad-pro-11-inch-wi-fi-128gb-silver/-/A-77616876?clkid=424d3f13N71d611ea882442010a246c11&lnm=201333&afid=NOOBPRO%20ASSOCIATES%20LLC&ref=tgt_adv_xasd0002"
    walmart = "https://www.walmart.com/ip/Apple-11-inch-iPad-Pro-2020-Wi-Fi-128GB-Silver/700142742"
    walmart_img_alt = "Apple 11-inch iPad Pro"
    model = "MY252LL-A"
    sub_name = f"{model}_ipad_pro_11_inch"
    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [ 
            BestBuy(self.sub_name, self.best_buy, product_type=self.product_type, msrp=self.msrp),
            BandH(self.sub_name, self.b_and_h, product_type=self.product_type, msrp=self.msrp),
            Target(self.sub_name, self.target, *self.target_keys, product_type=self.product_type, msrp=self.msrp),
            Walmart(self.sub_name, self.walmart, self.walmart_img_alt, product_type=self.product_type, msrp=self.msrp)
        ]

