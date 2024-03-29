# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class PropertiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # Primary Field
    title = Field()
    price = Field()
    image_urls = Field()

    # Calculated Fields
    images = Field()

    # HouseKeeping Fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()