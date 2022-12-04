from urllib.parse import urlencode
import scrapy
from chocolatesscraper.items import ChocolateProduct
from chocolatesscraper.itemloaders import ChocolateProductLoader
 
API_KEY = 'e0519c9a-073a-4e70-b111-b1b3a3a9480c'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url ='https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class ChocolatespiderSpider(scrapy.Spider):
    name = 'chocolatespider'
    allowed_domains = ['chocolate.co.uk']
    start_urls = ['http://chocolate.co.uk/collections/all']
    
    def start_requests(self):
        start_url = "https://www.chocolate.co.uk/collections/all"
        yield scrapy.Request(url=get_proxy_url(start_url),callback=self.parse)

    def parse(self, response):
        
        products = response.css('product-item')
        
        
        
        for product in products:
            
            chocalate = ChocolateProductLoader(item = ChocolateProduct(),selector = product)
            chocalate.add_css('name','a.product-item-meta__title::text'),
            chocalate.add_css('price','span.price',re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocalate.add_css('url','div.product-item-meta a::attr(href)')
            yield chocalate.load_item()
            
        next_page = response.css('[rel="next"] ::attr(href)').get()
        
        if next_page is not None:
            next_page_url='https://www.chocolate.co.uk' + next_page
            yield response.follow(get_proxy_url(next_page_url),callback=self.parse)

