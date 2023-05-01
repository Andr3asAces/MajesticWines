import scrapy

class WineSpider(scrapy.Spider):
    # this needs to inherit all methids from the scrapy.Spider class
    name = 'winespider' # referencing to my winespider.py
    start_urls= ['https://www.majestic.co.uk/red-wine'] # can be a list with many urls

    def parse(self, response):
        # self because is a function within this class
        # response will basically be the 'response' variable from scrapy that contains all webpage info
        # like we mentioned before everything done on the scrapy shell is saved on the response variable
        # which we will be passing here in order to transform the data to a nice format
        for products in response.css('div.product-box'):             
            # instead of 'return' as in normal py functions
            # scrapy objects use 'yield' 
            try: 
                yield { 
                'BottleName' : products.css("a.product-name.t-not-link::text").get(),
                'Price'      : products.css('div.product-price::text').get(),
                'Description': products.css("div.product-info-content.d-none::text").get(),
                'Link'       : products.xpath("div//a/@href").extract()
                    }
            except Exception:
                print('something didnt work') 
        next_page =  response.css('li.next-page>a').attrib['href'] 
        # in css '>' is used to go from the parent to the child node
        if next_page is not None:
            # if that page exists basically we get a response
            # we use the scray .follow() method to go to the next link
            # and we also want to add a callback that basically directs the response 
            # to go back to parse() and extract the info of the next page
            next_page = 'https://www.majestic.co.uk'+ str(next_page) 
            print(next_page)   
            yield response.follow(next_page, callback=self.parse ) 