from assets.products.base_product import BaseProduct
from assets.sources.source_clients.b_and_h import BandH
from assets.sources.source_clients.walmart import Walmart
from assets.sources.source_clients.amazon import AmazonUsed


class MicrosoftSurface(BaseProduct):
    bh = "https://www.bhphotovideo.com/c/product/1506690-REG/microsoft_vdv_00001_12_3_multi_touch_surface_pro.html"
    walmart = "https://www.walmart.com/ip/8GB-128GB-Editing-Extended-Standard-Pro-Touch-Elite-i5-1035G4-Intel-Surface-Suite-Platinum-Microsoft-Warranty-VDV-00001-Bundle-18-2-12-3-inch-Year-7-/482257773"
    amazon = "https://www.amazon.com/New-Microsoft-Surface-Pro-Touch-Screen/dp/B07YNHXX8D/ref=sr_1_1?dchild=1&keywords=model+%22VDV-00001%22&qid=1590716180&sr=8-1"

    model = "VDV-00001"
    sub_name = "VDV-00001_surface"
    walmart_product_image_alt = "Microsoft VDV-00001"

    product_type = "Tablet"

    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            BandH(self.sub_name, self.bh, product_type=self.product_type),
            Walmart(self.sub_name, self.walmart, self.walmart_product_image_alt, product_type=self.product_type),
            AmazonUsed(self.sub_name, self.amazon, product_type=self.product_type),
        ]