import scrapy
from scrapy_splash import SplashRequest

class SplashSpider(scrapy.Spider):
	name = "jsscraper"
	start_urls = ["http://quotes.toscrape.com/js/"]
	
	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 0.5})
	
	def parse(self, response):
		for q in response.css("div.quote"):
			yield {
				q.css(".author::text").get(),
				q.css(".text::text").get(),
				}