from assets.products.base_product import BaseProduct
from assets.sources.source_clients.amazon import Amazon
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.newegg import NewEgg
from assets.sources.source_clients.newegg import NewEggRefurbished
from assets.sources.source_clients.walmart import Walmart
from assets.sources.source_clients.walmart import WalmartRefurbished
from assets.sources.source_clients.b_and_h import BandH
from assets.sources.source_clients.decluttr import Decluttr

class MacBookAir2020(BaseProduct):
    best_buy = "https://www.bestbuy.com/site/apple-macbook-air-13-3-laptop-with-touch-id-intel-core-i3-8gb-memory-256gb-solid-state-drive-latest-model-gold/6366612.p?skuId=6366612"
    walmart = "https://www.walmart.com/ip/Apple-13-3-MacBook-Air-2020-Gold-Wallet-Reader-MagicMouse2-USBHUB/201580499"
    amazon = (
        "https://www.amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08632W2H6?th=1"
    )
    bh = "https://www.bhphotovideo.com/c/product/1553858-REG/apple_mwtl2ll_a_13_3_macbook_air_with.html"
    newegg = "https://www.newegg.com/p/2SN-0001-014E4?Description=MWTL2LL%2fA&cm_re=MWTL2LL%2fA-_-2SN-0001-014E4-_-Product&quicklink=true"
    model = "MWTL2LL-A"
    sub_name = "MWTL2LL-A_macbook_air_2020"
    walmart_product_image_alt = "MacBook Air 2020 Gold"
    walmart_tuple = (
        walmart,
        walmart_product_image_alt,
    )
    product_type = "Computer"
    # MSRP found at under Global Price Tab https://everymac.com/systems/apple/macbook-air/specs/macbook-air-core-i3-1.1-dual-core-13-retina-display-2020-scissor-specs.html#macspecs3
    msrp = "1000"

    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BestBuy(self.sub_name, self.best_buy, product_type=self.product_type, msrp=self.msrp),
            #NewEgg(self.sub_name, self.newegg, product_type=self.product_type, msrp=self.msrp),
            Walmart(self.sub_name, *self.walmart_tuple, product_type=self.product_type, msrp=self.msrp),
            Amazon(self.sub_name, self.amazon, product_type=self.product_type, msrp=self.msrp),
            #BandH(self.sub_name, self.bh, product_type=self.product_type, msrp=self.msrp),
        ]

# Decluttr sells refurbished products.
# The model chosen for the MacBOokAir2019 Space Gray i5 128GB
# to make ease of calculation of MSRP better.
# Source of truth: https://prices.appleinsider.com/apple-macbook-air-2019
# (Apple's website was confusing and tries to get you to buy new
# which is why this website is used)
# MSRP listed at 1099.00

class MacBookAir2019(BaseProduct):
    decluttr_js = "return Array.from(document.getElementsByClassName('product-box')).filter(e => e.textContent.includes('2019') && e.textContent.includes('MacBook Air'))"
    decluttr = "https://www.decluttr.com/us/store/category/computers-and-accessories/#prm_creative=iMacs-MacBooks&prm_name=iMacs-MacBooks-HP&prm_position=S3&prm_id=HPS3N"
    best_buy = "https://www.bestbuy.com/site/apple-macbook-air-13-3-laptop-with-touch-id-intel-core-i5-8gb-memory-128gb-solid-state-drive-space-gray/6356906.p?skuId=6356906"
    walmart = "https://www.walmart.com/ip/Refurbished-M-cBook-A-r-13-3-Laptop-with-Touch-ID-Intel-Core-i5-8GB-RAM-128GB-2019-Space-Gray-MVFH2LL-A/525081370"
    newegg = "https://www.newegg.com/p/2SN-0001-012E1?Description=MVFH2LL%2fA&cm_re=MVFH2LL%2fA-_-2SN-0001-012E1-_-Product&quicklink=true"
    model = "MVFH2LL-A"
    sub_name = "MVFH2LL-A_macbook_air_2019"
    product_type = "Computer"
    walmart_product_image_alt = "Refurbished MаcBook Aіr"
    walmart_tuple = (
        walmart,
        walmart_product_image_alt,
    )

    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BestBuy(self.sub_name, self.best_buy),
            Decluttr(self.sub_name, self.decluttr, self.decluttr_js),
            WalmartRefurbished(self.sub_name, *self.walmart_tuple),
            NewEggRefurbished(self.sub_name, self.newegg),
        ]

