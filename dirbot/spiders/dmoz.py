import scrapy
import re

from dirbot.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.urbanpro.com"]
    start_urls = [
        "https://www.urbanpro.com/school/search?city=Hyderabad&area=&keyword=&type=&topicId=573&offset=00&max=10",
    ]

    def parse(self, response):
        for sel in response.xpath('/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/div'):
            title = map(unicode.strip, sel.xpath('div[2]/div[2]/div[1]/div[1]/p/a/@href').extract() )
            
            if(len(title)> 0):
                titles = title[0].encode('ascii')



            ##print titles

            if len(titles) > 3:
                url = response.urljoin(titles)                               
                yield scrapy.Request(url, callback=self.parse_dir_contents)
            
        for sel in response.xpath('/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/div[13]/a'):
            game = sel.xpath('text()').extract()
            games=game[0].encode('ascii')

            if games == "Next":
                palm = sel.xpath('@href').extract()
                palms = palm[0].encode('ascii')
                
                url = response.urljoin(palms)      
                     
                yield scrapy.Request(url, callback=self.parse)
        
        
    


   



    def parse_dir_contents(self, response):

        ##Name works fine... Fuck off from here
        item = DmozItem()
        item['name'] = " ".join(response.xpath('/html/body/div[2]/div/div/div/div/div/div[4]/div[1]/h1/text()').extract()[0].split())

        

        ##Locality works fine ... Fuck off from here
            
        funk = response.xpath('/html/body/div[2]/div/div/div/div/div/div[5]/div[1]/div[1]/a/text()').extract()
        for k in funk:
            temp = k.encode('ascii')
            item["Locality"] = temp


       
        
                
        
        for sel in response.xpath('/html/body/div[2]/div/div/div/div/div/div[5]/div[1]/div[1]/p'):
            temp =  sel.xpath('b/text()').extract()[0].encode('ascii').split(':')

           
            fields = temp[0]
            field = fields.split(' ')
            fields = field[0]



            
            ##Working till here
            


            ##Address works fine .. Fuck off from here
            if fields == 'Address':
                item["Address"]=  " ".join(sel.xpath('text()').extract()[1].encode('ascii').split())

                

            if fields == 'Landmark':
                item["Landmark"] = " ".join(sel.xpath('text()').extract()[1].split())
            

            ##Email works fine .. Fuck off from here
            if fields == 'Email':
                f = sel.xpath('a/@href').extract()[0].split(':')
                item["Email"] = f[1]

            if fields == 'Web':
                item["Web"] = " ".join(sel.xpath('a/@href').extract()[0].split())
                



            ## Phone is working
            if fields == 'Phone' :
                item["Phone"] = " ".join(sel.xpath('text()').extract()[1].split())
                
                
            

            
            
        yield item

          

            

                        
                




           ## item[fields] = sel.xpath('text()').extract()
            
        ##print item['name'][0].encode('ascii')