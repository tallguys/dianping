# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    title = scrapy.Field()
    cost = scrapy.Field()
    shopAddress = scrapy.Field()
    distanceInfo = scrapy.Field()
    distance = scrapy.Field()
    score = scrapy.Field()
    shopName = scrapy.Field()
    shopType = scrapy.Field()
    tagId = scrapy.Field()
    tagName = scrapy.Field()
    like = scrapy.Field()
    apply_result = scrapy.Field()

    pass
