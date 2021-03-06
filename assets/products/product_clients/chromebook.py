from assets.products.base_product import BaseProduct
from assets.sources.source_clients.amazon import Amazon
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.comp_usa import CompUSA
from assets.sources.source_clients.walmart import Walmart


class HPTouchScreenChromebook(BaseProduct):
    best_buy = "https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-core-i3-8gb-memory-64gb-emmc-flash-memory-white/6365772.p?skuId=6365772"
    walmart = "https://www.walmart.com/ip/HP-2-in-1-14-Full-HD-Touchscreen-Chromebook-x360-Core-i3-8130U-8GB-RAM-64GB-eMMC/814497767"
    amazon = "https://www.amazon.com/HP-Chromebook-x360-14-FHD-Touch/dp/B08121BNBS"
    model = "14-DA0012DX"
    sub_name = "14DA0012DX_hp_chromebook"
    walmart_product_image_alt = "HP 2-in-1 14"
    walmart_tuple = (
        walmart,
        walmart_product_image_alt,
    )
    product_type = "Computer"
    # HP no longer sells, MSRP taken from "was" price at https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-core-i3-8gb-memory-64gb-emmc-flash-memory-white/6365772.p?skuId=6365772
    msrp="599"
    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BestBuy(self.sub_name, self.best_buy, product_type=self.product_type, msrp=self.msrp),
            Walmart(self.sub_name, *self.walmart_tuple, product_type=self.product_type, msrp=self.msrp),
            Amazon(self.sub_name, self.amazon, product_type=self.product_type, msrp=self.msrp),
        ]
