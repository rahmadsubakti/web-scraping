# Downlao images from zerochan
# using requests, beautiful soup, and urllib

import requests
from bs4 import BeautifulSoup as bs
import urllib.parse as parse
import urllib.request as r
import urllib
import logging
import argparse
import concurrent.futures
import json
import os

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class ZerochanScraper:

	def __init__(self, url=None):
		self.url = url
		self.count = 1
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.folder = ''
		self.undownload = []

	def _url(self, url):
		# Input url
		self.url = url

	def parse(self, soup):
		# Parse image
		images = soup.find('ul', attrs={'id': 'thumbs2'}).find_all('li')
		links = [image.p.a['href'] for image in images if image.p.a]
		return links

	def download(self, link):
		path = parse.urlsplit(link)
		filename = parse.unquote(path.path.split('/')[-1])

		try:
			r.urlretrieve(link, self.folder+filename)
		except urllib.error.HTTPError:
			logging.warning(f'{link} not found')
		except:
			# write undownloaded links to file
			self.undownload.append(link)
		else:
			message = f'{self.count} - {filename} Downloaded'
			logging.warning(message)
			self.count += 1

	def download_threads(self, links):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.map(self.download, links)

	def start(self, undownload=False):
		self.read_checkpoint()

		# Downloading process
		while True:
			try:
				requested = requests.get(self.url)
			except Exception as e:
				self.create_checkpoint()
				logging.warning(e)
				os._exit(0)

			soup = bs(requested.content, 'html5lib')
			links = self.parse(soup)
			self.download_threads(links)

			next_url = soup.find('p', attrs={'class': 'pagination'}).find('a', attrs={'rel': 'next'})
			if next_url:
				self.url = parse.urljoin(self.url, next_url['href'])
			else:
				logging.warning('Download complete!')

				if len(self.undownload) != 0:
					undowloaded_dict = {'links': self.undownload}
					with open('undownloaded.json', 'w') as json_file:
						json.dump(undowloaded_dict, json_file)
				break

	def create_checkpoint(self):
		# if request getting error, write file contains a link of a page
		with open('checkpoint.txt', 'w') as f:
			f.write(self.url)

	def read_checkpoint(self):
		# check if checkpoint file is exist
		checkpoint_file_path = os.path.join(self.dir_path, 'checkpoint.txt')
		if os.path.isfile(checkpoint_file_path):
			with open(checkpoint_file_path, 'r') as f:
				self.url = f.readlines()[-1]

	def create_dir(self, directory='zerochan'):
		# create folder contain images
		path = os.path.join(self.dir_path, directory)
		try:
			os.mkdir(path)
		except:
			pass
		self.folder = directory + '/'

	def download_undownloaded(self):
		with open('undownloaded.json', 'r') as f:
			links = json.load(f)
			links = links['links']
		self.download_threads(links)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', help='Zerochan URL to scrape')
	parser.add_argument('-d', '--dir', help='Name of directory for containing all your downloaded images')
	parser.add_argument('-f')
	args = parser.parse_args()

	scraper = ZerochanScraper()
	if args.dir:
		scraper.create_dir(args.dir)
	else:
		scraper.create_dir()

	if args.url is None and args.f:
		scraper.download_undownloaded()
	elif args.url:
		scraper._url(args.url)
		scraper.start()
	else:
		raise SyntaxError("""Please provide url about a topic on zerochan or type '-f' if you
							have 'undownloaded.json' file""")
