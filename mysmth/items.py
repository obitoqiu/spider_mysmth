# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 需要存储的字段
class MysmthItem(scrapy.Item):
    # define the fields for your item here like:
    msgid = scrapy.Field()
    refid = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
    pubtime = scrapy.Field()

