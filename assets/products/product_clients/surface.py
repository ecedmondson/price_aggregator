from assets.products.base_product import BaseProduct
from assets.sources.source_clients.b_and_h import BandH
from assets.sources.source_clients.walmart import Walmart
from assets.sources.source_clients.amazon import AmazonUsed
from assets.sources.source_clients.newegg import NewEgg

class MicrosoftSurface(BaseProduct):
    bh = "https://www.bhphotovideo.com/c/product/1506690-REG/microsoft_vdv_00001_12_3_multi_touch_surface_pro.html"
    walmart = "https://www.walmart.com/ip/8GB-128GB-Editing-Extended-Standard-Pro-Touch-Elite-i5-1035G4-Intel-Surface-Suite-Platinum-Microsoft-Warranty-VDV-00001-Bundle-18-2-12-3-inch-Year-7-/482257773"
    amazon = "https://www.amazon.com/New-Microsoft-Surface-Pro-Touch-Screen/dp/B07YNHXX8D/ref=sr_1_1?dchild=1&keywords=model+%22VDV-00001%22&qid=1590716180&sr=8-1"
    newegg = "https://www.newegg.com/platinum-microsoft-surface-pro-7-vdv-00001/p/N82E16834736092?Description=VDV-00001&cm_re=VDV-00001-_-34-736-092-_-Product"

    model = "VDV-00001"
    sub_name = "VDV-00001_surface"
    walmart_product_image_alt = "Microsoft VDV-00001"

    product_type = "Tablet"
    #https://www.microsoft.com/en-us/p/surface-pro-7/8n17j0m5zzqs?activetab=overview&ranMID=24542&ranEAID=yr7LsPS5ySE&ranSiteID=yr7LsPS5ySE-LYuEGrD7TqnnAwRbegLCeg&epi=yr7LsPS5ySE-LYuEGrD7TqnnAwRbegLCeg&irgwc=1&OCID=AID2000142_aff_7593_1243925&tduid=%28ir__pxvan2txe9kftmdckk0sohzg2u2xnqsmjt0pbkfq00%29%287593%29%281243925%29%28yr7LsPS5ySE-LYuEGrD7TqnnAwRbegLCeg%29%28%29&irclickid=_pxvan2txe9kftmdckk0sohzg2u2xnqsmjt0pbkfq00
    msrp = "749"

    def __init__(self):
        super().__init__()
        self.clients = self.get_clients()
        self.products = self.get_all_products()

    def get_clients(self):
        return [
            NewEgg(self.sub_name, self.newegg, product_type=self.product_type, msrp=self.msrp),
            BandH(self.sub_name, self.bh, product_type=self.product_type, msrp=self.msrp),
            Walmart(self.sub_name, self.walmart, self.walmart_product_image_alt, product_type=self.product_type, msrp=self.msrp),
            AmazonUsed(self.sub_name, self.amazon, product_type=self.product_type, msrp=self.msrp),
        ]