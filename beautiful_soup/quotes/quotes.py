import requests
import html5lib
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import json

def parse(soup):
    global quotes
    global authors
    for quote in soup.findAll('div', attrs={'class': 'quote'}):
        text = quote.find('span', attrs={'class': 'text'}).text
        author = quote.find('small', attrs={'class': 'author'}).text
        t_dict = {'text': text, 'author': author}
        quotes.append(t_dict)

url = 'http://quotes.toscrape.com'
r = requests.get(url)
soup = bs(r.content, 'html5lib')
quotes = []
#print(soup.prettify())
parse(soup)

while True:
    try:
        next_page = soup.find('li', attrs={'class': 'next'}).a['href']
    except:
        break
    else:
        next_url = urljoin(url, next_page)
        r = requests.get(next_url)
        soup = bs(r.content, 'html5lib')
        parse(soup)

with open('quotes.json', 'w') as f:
    json.dump(quotes, f)