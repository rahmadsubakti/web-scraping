from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class BabyNameScraper:

	def __init__(self):
		options = Options()
		options.headless = True
		caps = DesiredCapabilities().FIREFOX
		caps['pageLoadStrategy'] = 'eager'
		self.browser = webdriver.Firefox(options=options, desired_capabilities=caps, 
										executable_path='E:/aplikasi_software/geckodriver/geckodriver.exe')
		self.url = 'https://www.babynames.com/boy-names'
		self.df = pd.DataFrame(columns=['name', 'gender', 'origin', 'meaning'])

	def parse(self, soup):
		name_links = soup.find_all('a', attrs={'class': 'M'})
		for link in name_links:
			link = link['href']
			link = urljoin(self.url, link)
			r = requests.get(link)
			if r.status_code != 200 or r.url != link: # if unable to get response or url requested is not same (not work on link that has been shorten)
				continue
			yield r
			
	def parse_r(self, soup):
		for link in self.parse(soup):
			soup_name = bs(link.content, 'html5lib')
			message = f'Scraping {link.url}'
			logging.warning(message)
			name = soup_name.find('h1', attrs={'class': 'baby-name'}).text
			div = soup_name.find_all('div', attrs={'class': 'name-meaning'})
			gender = div[0].a.text
			origin = div[1].a.text
			meaning = div[2].strong.text
			d = {'name': [name], 'gender': [gender], 'origin': [origin], 'meaning': [meaning]}
			yield d

	def to_csv(self, soup):
		for d in self.parse_r(soup):
			d = pd.DataFrame(d)
			self.df = self.df.append(d, ignore_index=True)
			self.df.to_csv('boy_names.csv')

	def start(self):
		self.browser.get(self.url)
		soup = bs(self.browser.page_source, 'html5lib')
		self.to_csv(soup)

		while True:
			try:
				next = self.browser.find_element_by_class_name('next-btn')
			except:
				logging.warning('Scraping Done!')
				break
			else:
				self.browser.execute_script('window.scrollBy(0, 900);')
				next.click()
				soup = bs(self.browser.page_source, 'html5lib')
				self.to_csv(soup)

	def __del__(self):
		self.browser.close()

scraper = BabyNameScraper()
try:
	scraper.start()
except Exception as e:
	logging.warning(e)
	#del scraper