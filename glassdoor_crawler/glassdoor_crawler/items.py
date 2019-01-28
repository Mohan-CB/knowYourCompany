# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
class Review(Item):
    # define the fields for your item here like:
    time = scrapy.Field()
    companyName = scrapy.Field()
    title = scrapy.Field()
    starRating = scrapy.Field()
    job = scrapy.Field()
    summary = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    uid = scrapy.Field()
    pass
