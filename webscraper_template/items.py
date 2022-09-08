# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperTemplateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QuotesItem(scrapy.Item):
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()