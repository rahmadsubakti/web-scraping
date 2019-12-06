# -*- coding: utf-8 -*-
import scrapy
from properties.items import PropertiesItem
from scrapy.loader import ItemLoader
import socket
import datetime
class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['books']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        """This function parses a property page
        @url http://books.toscrape.com
        @returns items 1
        @scrapes title price image_urls 
        @scrapes url project spider server date
        """
        l = ItemLoader(PropertiesItem(), response=response)
        l.add_css('title', '.product_pod a::attr(title)')
        l.add_css('price', '.product_pod p.price_color::text', re_first='[.0-9]+')
        l.add_css('image_urls', '.product_pod img::attr(src)')
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        return l.load_item()

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').get()
        return FormRequest.from_response(response, formdata={
            'csrf_token':token,
            'username': 'foobar',
            'password': 'foobar',}, 
            callback=self.parse_display)

    def parse_display(self, response):
        open_in_browser(response)