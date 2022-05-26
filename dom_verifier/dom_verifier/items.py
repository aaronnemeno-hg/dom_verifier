# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    status_code = scrapy.Field()
    gt_src = scrapy.Field()
    gt_code = scrapy.Field()
    pixel_src = scrapy.Field()
    pixel_code = scrapy.Field()