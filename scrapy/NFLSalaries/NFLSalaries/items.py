# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags

# Converting Salary to int type
def clean_amount(value):
    return int(value.replace(',', '').replace('$', ''))

def to_number(value):
    if value != "":
        return int(value)
    return None

class ContractItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    player = Field()
    team = Field()
    position = Field()
    age = Field(input_processor=MapCompose(remove_tags, to_number))
    total_value = Field(input_processor=MapCompose(remove_tags, clean_amount))
    avg_year = Field(input_processor=MapCompose(remove_tags, clean_amount))
    total_guaranteed = Field(input_processor=MapCompose(remove_tags, clean_amount))
    fully_guaranteed = Field(input_processor=MapCompose(remove_tags, clean_amount))
    free_agency_year = Field(input_processor=MapCompose(remove_tags, lambda value: value.split()[0], to_number))