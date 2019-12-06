from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup
import csv


options = Options()
options.headless = True
#browser = webdriver.Firefox(options=options, executable_path='C:\Program Files\Mozilla Firefox\geckodriver.exe')
browser = webdriver.Firefox()
browser.get('https://www.babynames.com/boy-names')

def parse(w, link_el):
	baby_names = []
	for a in link_el:
		print('Scraping: ', a)
		r = requests.get(a.get_attribute('href'))
		soup = BeautifulSoup(r.content, 'html5lib')
		name_header = soup.find('div', attrs={'class':'namepageheader'})
		desc = {'Name':name_header.h1.text}
	
		for row in name_header.findAll('div', attrs={'class':'name-meaning'}):
			k, v = row.text.split(': ')
			desc[k] = v
		
		baby_names.append(desc)
	
	for name in baby_names:
		w.writerow(name)
	
# get next button element, scroll to it, and click it
filename = 'boys1.csv'
with open(filename, 'w') as f:
	w = csv.DictWriter(f, ['Name', 'Gender', 'Origin', 'Meaning'])
	w.writeheader()
	while True:
		try:
			next = browser.find_element_by_class_name('next-btn')
			link_el = browser.find_elements_by_class_name('M')
			parse(w, link_el)
			browser.execute_script('window.scrollBy(0, 900);')
			next.click()
		except:
			browser.close()
			break
