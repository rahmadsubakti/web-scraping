# -*- coding: utf-8 -*-
import scrapy
from zerochan.items import ZerochanItem

class EeveeImageSpider(scrapy.Spider):
	name = 'image'
	start_urls = ['https://www.zerochan.net/Moemon']

	def parse(self, response):
		for image in response.css('ul#thumbs2 li'):
			image_url = image.css('a::attr(href)').getall()[-1]
			yield {'image_urls': [image_url]}
			
		next_page = response.css('p.pagination a::attr(href)').getall()[-1]
		if next_page is not None:
			href = response.urljoin(next_page)
			yield scrapy.Request(href, callback=self.parse)