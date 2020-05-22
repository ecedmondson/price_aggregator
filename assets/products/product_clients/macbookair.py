from assets.products.base_product import BaseProduct
from assets.sources.source_clients.amazon import Amazon
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.newegg import NewEgg
from assets.sources.source_clients.walmart import Walmart
from assets.sources.source_clients.b_and_h import BandH


class MacBookAir2020(BaseProduct):
    best_buy = "https://www.bestbuy.com/site/apple-macbook-air-13-3-laptop-with-touch-id-intel-core-i3-8gb-memory-256gb-solid-state-drive-latest-model-gold/6366612.p?skuId=6366612"
    walmart = "https://www.walmart.com/ip/Apple-13-3-MacBook-Air-2020-Gold-Wallet-Reader-MagicMouse2-USBHUB/201580499"
    amazon = (
        "https://www.amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08632W2H6?th=1"
    )
    bh = "https://www.bhphotovideo.com/c/product/1553858-REG/apple_mwtl2ll_a_13_3_macbook_air_with.html"
    newegg = "https://www.newegg.com/p/2SN-0001-014E4?Description=MWTL2LL%2fA&cm_re=MWTL2LL%2fA-_-2SN-0001-014E4-_-Product&quicklink=true"
    model = "MWTL2LL-A"
    sub_name = "MWTL2LL-A_macbook_air"
    walmart_product_image_alt = "MacBook Air 2020 Gold"
    walmart_tuple = (
        walmart,
        walmart_product_image_alt,
    )
    product_type = "Computer"

    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BestBuy(self.sub_name, self.best_buy),
            NewEgg(self.sub_name, self.newegg),
            Walmart(self.sub_name, *self.walmart_tuple),
            Amazon(self.sub_name, self.amazon),
            BandH(self.sub_name, self.bh),
        ]
