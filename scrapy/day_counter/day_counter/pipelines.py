# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

class DayCounterPipeline(object):
    DAYS = ('Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday')

    def __init__(self):
        self.day = {}

    def process_item(self, item, spider):
        day_idx = datetime.strptime(item['day'], '%B %d, %Y').weekday()
        day = self.DAYS[day_idx]
        if day not in self.day:
            self.day[day] = 1
        else:
            self.day[day] += 1
        return self.day
