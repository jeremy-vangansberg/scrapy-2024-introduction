# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookscraperItem(scrapy.Item):
    title = scrapy.Field()
    upc = scrapy.Field()
    price = scrapy.Field()
