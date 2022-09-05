# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RegulationsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = 'regulation'
    title = scrapy.Field()
    postDate = scrapy.Field()
    rid = scrapy.Field()

class RegulationsDetailItem(scrapy.Item):
    type = 'comment'
    comment = scrapy.Field()
    postDate = scrapy.Field()
    cid = scrapy.Field()
    poster = scrapy.Field()