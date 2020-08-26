import scrapy
import datetime

# Year: >= 2014
# Mileage <= 110,000 km
# Carfax?
# Price: <= $13000

# Obtain prices and other pertinent data from above from various dealerships
# Inspect various HTML scheme, feed into CSV
# CSV feeds into Regressor, use Regressor to evaluate slopes ($ per)

# scrapy runspider scraper.py -o scraped.csv

class CarSpider(scrapy.Spider):

    name = 'car_scraper'
    allowed_domains = ['markhamhonda.com']
    start_urls = ['https://www.markhamhonda.com/en/used-inventory/honda/civic/2016']

    def parse(self,response):
        # Title
        car_title = response.xpath('//div[@class="inventory-tile-section-main-picture"]/a/@title').getall()
        # Link
        car_url = response.xpath('//div[@class="inventory-tile-section-main-picture"]/a/@href').getall()
        # Price
        car_price = [i.strip() for i in response.xpath('//div[@class="vehicle-current-price  inventory-tile-section-price__sale-price"]/span[@itemprop="price"]/text()').getall()]

        row_data = zip(car_title, car_url, car_price)

        for item in row_data:
            scraped_info = {
            'Car Title': item[0],
            'Car URL' : item[1],
            'Car Price': item[2]
            }

            yield scraped_info

    custom_settings = {
    'FEED_FORMAT':"csv",
    "FEED_URI":f"cars_scraped {str(datetime.date.today())}.csv"
    }
# class CarSpider(scrapy.Spider):
#     name = "quotes"
#
#     def start_requests(self):
#         urls = [
#             'http://quotes.toscrape.com/page/1/',
#             'http://quotes.toscrape.com/page/2/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)

make = "honda"
model = "civic"
year = "2016"
page = "?page=2"
url = f"https://www.markhamhonda.com/en/used-inventory/{make}/{model}/{year}"
