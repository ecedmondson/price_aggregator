from assets.products.product import BaseProduct
from assets.sources.source_clients.amazon import Amazon
from assets.sources.source_clients.best_buy import BestBuy
from assets.sources.source_clients.comp_usa import CompUSA
from assets.sources.source_clients.walmart import Walmart


class HPTouchScreenChromebook(BaseProduct):
	best_buy = "https://www.bestbuy.com/site/hp-2-in-1-14-touch-screen-chromebook-intel-core-i3-8gb-memory-64gb-emmc-flash-memory-white/6365772.p?skuId=6365772"
    comp_usa = "https://www.compusa.com/deals/8638-BestBuy-14-HP-2-in-1-Touch-Screen-Chromebook-Intel-Core-i3-8130U-8GB-Memory-64GB-eMMC-Flash-Memory-Intel-UHD-Graphics-620-Chrome-OS-14-DA0012DX"
    walmart = "https://www.walmart.com/ip/HP-2-in-1-14-Full-HD-Touchscreen-Chromebook-x360-Core-i3-8130U-8GB-RAM-64GB-eMMC/814497767"
    amazon = "https://www.amazon.com/HP-Chromebook-x360-14-FHD-Touch/dp/B08121BNBS"
    model = "14-DA0012DX"
    sub_name = "14DA0012DX_hp_chromebook"
    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients():
        return [BestBuy(self.best_buy, "6365772"), CompUSA(self.comp_usa), Walmart(self.walmart, "HP 2-in-1 14"), Amazon(self.amazon, )]