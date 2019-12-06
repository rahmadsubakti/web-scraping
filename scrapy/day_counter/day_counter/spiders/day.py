# -*- coding: utf-8 -*-
import scrapy
from day_counter.items import DayCounterItem
from datetime import datetime

class DaySpider(scrapy.Spider):
    name = 'day'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['http://blog.scrapinghub.com/']

    DAYS = ('Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday')

    days_dict = {}

    def parse(self, response):
        
        for date in response.css('span.date'):
            day = date.css('a::text').get().strip()
            dt_idx = datetime.strptime(day, '%B %d, %Y').weekday()
            dt = self.DAYS[dt_idx]
            if dt not in self.days_dict:
                self.days_dict[dt] = 1
            else:
                self.days_dict[dt] += 1

        older_posts = response.css('.next-posts-link::attr(href)').get()
        if older_posts:
            yield response.follow(older_posts, callback=self.parse)
        else:
            for day, num in self.days_dict.items():
                yield {'day': day, 'num': num}