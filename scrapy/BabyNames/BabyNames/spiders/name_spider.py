import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from scrapy_selenium import SeleniumRequest
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC

class BoyBabyNamesSpider(scrapy.Spider):
	name = 'boy-names'
	start_urls = ['https://www.babynames.com/boy-names']
	
	def __init__(self):
		#options = Options()
		#options.headless = True
		self.browser = webdriver.Firefox()
		
	def parse(self, response):
		self.browser.get(self.start_urls[0])
		
		while True:
			for name in self.browser.find_elements_by_class_name('M'):
					url = name.get_attribute('href')
					yield scrapy.Request(url, callback=self.parse_link)
			try:
				next = self.browser.find_element_by_class_name('next-btn')
			except:
				break
			else:
				self.browser.execute_script('window.scrollBy(0, 900);')
				next.click()
		
		
		#yield SeleniumRequest(url=self.start_urls[0], 
		#						callback=self.parse_link, 
		#						wait_until=EC.element_to_be_clickable((By.CLASS_NAME,'next_btn')),
		#						script='window.scrollBy(0, 900);',
		#					)
		
	def parse_link(self, response):
		for href in response.css('a.M::attr(href)'):
			yield response.follow(href, callback=self.parse_name)
			
	def parse_name(self, response):
		yield {
			'name': response.css('h1.baby-name::text').get(),
			'gender': response.css('div.name-meaning a::text').getall()[0],
			'origin': response.css('div.name-meaning a::text').getall()[1],
			'meaning': response.css('div.name-meaning strong::text').get(),
		}
		
	def __del__(self):
		self.browser.close()