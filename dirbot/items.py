from scrapy.item import Item, Field


class DmozItem(Item):

    name = Field()
    Address = Field()
    Locality = Field()
    Web = Field()
    Landmark = Field()
    Phone = Field()
    Email = Field()
    
    

