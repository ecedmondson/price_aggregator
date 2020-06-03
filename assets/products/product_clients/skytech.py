from assets.products.base_product import BaseProduct
from assets.sources.source_clients.amazon import Amazon
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.newegg import NewEgg
from assets.sources.source_clients.skytech import Skytech as STClient

# So, we are technically scraping the manufacturer for this product.
# This, however, provides us with a nice source of truth for MSRP.
# MSRP at skytech_url and was 974.99 as of 5/27/2020.

class Skytech(BaseProduct):
    best_buy = "https://www.bestbuy.com/site/skytech-gaming-archangel-gaming-desktop-amd-ryzen-5-3600-16gb-memory-nvidia-geforce-gtx-1660-super-500gb-ssd-white/6408494.p?skuId=6408494"
    skytech_url = "https://skytechgaming.com/product/archangel-3-0-amd-ryzen-5-3600-nvidia-gtx-6gb-gddr5-500gb-ssd-8gb-ram/"
    amazon = "https://www.amazon.com/Skytech-Archangel-Gaming-Computer-Desktop/dp/B085X2DCBT/ref=zg_bsnr_565098_5?_encoding=UTF8&psc=1&refRID=BPAGM29YZKQHT8YKRZN6"
    newegg = "https://www.newegg.com/skytech-st-arch3-0-0056-ne-archangel/p/N82E16883289049?Description=skytech%20archangel&cm_re=skytech_archangel-_-83-289-049-_-Product&quicklink=true"
    model = "ST-Arch3.0-0056-NE"
    sub_name = f"skytech_gaming_{model.replace('-', '_')}"
    product_type = 'Computer'
    msrp="975"
    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BestBuy(self.sub_name, self.best_buy, product_type=self.product_type, msrp=self.msrp), 
            NewEgg(self.sub_name, self.newegg, product_type=self.product_type, msrp=self.msrp),
            STClient(self.sub_name, self.skytech_url, product_type=self.product_type, msrp=self.msrp),
            Amazon(self.sub_name, self.amazon, product_type=self.product_type, msrp=self.msrp),
        ]
