# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniversalSpiderItem(scrapy.Item):
    jobinfo = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    postcode = scrapy.Field()
    description = scrapy.Field()
    pass

