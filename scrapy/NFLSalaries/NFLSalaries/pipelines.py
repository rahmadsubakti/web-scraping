# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class NflsalariesPipeline(object):
    def __init__(self):
        self.players = set()
    def process_item(self, item, spider):
        if item['player'] in self.players:
            raise DropItem("This player has been stored: %s" % item)
        else:
            self.players.add(item['player'])
        return item
