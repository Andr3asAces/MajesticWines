import scrapy

class ContactSpider(scrapy.Spider):
    # this needs to inherit all methids from the scrapy.Spider class
    name = 'ContactSpider' # referencing to my ContactSpider.py
    start_urls= ['https://www.google.co.uk/search?q=title:gmail.com+OR+yahoo.com+%22England%22+site:https://www.linkedin.com/in/&lr=&safe=images&as_qdr=all&sxsrf=APq-WBs8_ACDHUZF6HZuIPfYhxWY94-0gw:1647271574939&ei=ll4vYqzkONr6gAbZ0KSQCg&start=0&sa=N&ved=2ahUKEwish8ro9MX2AhVaPcAKHVkoCaI4KBDy0wN6BAgBEDo&biw=939&bih=961&dpr=1'] # can be a list with many urls

    def parse(self, response):
        # self because is a function within this class
        # response will basically be the 'response' variable from scrapy that contains all webpage info
        # like we mentioned before everything done on the scrapy shell is saved on the response variable
        # which we will be passing here in order to transform the data to a nice format
        for contact in response.css('div.contact-box'):             
            # instead of 'return' as in normal py functions
            # scrapy objects use 'yield' 
            try: 
                yield { 
                'BottleName' : contacts.css("a.contact-name.t-not-link::text").get(),
                'Price'      : contacts.css('div.contact-price::text').get(),
                'Description': contacts.css("div.contact-info-content.d-none::text").get(),
                'Link'       : contacts.xpath("div//a/@href").extract()
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