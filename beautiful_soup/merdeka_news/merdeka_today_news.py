import requests
from bs4 import BeautifulSoup as bs
import html5lib
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
"""
url = 'https://www.merdeka.com/berita-hari-ini/'

r = requests.get(url)
r_url = r.url
soup = bs(r.content, 'html5lib')

news = []
def parse(soup):
	global news
	global r_url
	list_news = soup.findAll('div', attrs={'class': 'mdk-tag-contg'})
	for item in list_news:
		category = item.find('span', attrs={'style': 'color:#666666;'}).text
		title = item.find('div', attrs={'class': 'mdk-tag-contln-titlebar'}).a.text
		news.append({'category': category, 'title': title})
		message = f'scraped items at {r_url}'
		logging.warning(message)

parse(soup)

while True:
	try:
		next_page = soup.find('div', attrs={'class': 'paging-container'}).a['href']
	except:
		break
	else:
		r = requests.get(next_page)
		r_url = r.url
		soup = bs(r.content, 'html5lib')
		parse(soup)"""


#with open('today_news.json', 'w') as f:
#	json.dump(news, f)

class Scraper:
	def __init__(self):
		self.url = 'https://www.merdeka.com/berita-hari-ini/'
		self.news = []

	def parse(self, soup):
		list_news = soup.findAll('div', attrs={'class': 'mdk-tag-contg'})
		for item in list_news:
			category = item.find('span', attrs={'style': 'color:#666666;'}).text
			title = item.find('div', attrs={'class': 'mdk-tag-contln-titlebar'}).a.text
			self.news.append({'category': category, 'title': title})
			message = f'scraped items at {self.url.url}'
			logging.warning(message)

	def start(self):
		self.url = requests.get(self.url)
		soup = bs(self.url.content, 'html5lib')
		self.parse(soup)

		while True:
			try:
				self.url = soup.find('div', attrs={'class': 'paging-container'}).find('a', attrs={'class': 'link_next'})['href']
			except:
				logging.warning('Scraper done!')
				break
			else:
				self.url = requests.get(self.url)
				soup = bs(self.url.content, 'html5lib')
				self.parse(soup)

scraper = Scraper()
scraper.start()