import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quotes" # in shell -> scrapy crawl [name]

    # How to give url
    # 1. Write method start request like this:
    """
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)"""

    # 2. use variable named 'start_urls' and assign with list object. Commented to see how filtering works
    """
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        # 'http://quotes.toscrape.com/page/2/', # commented for implement next link
    ]"""

    def __init__(self, author=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author.replace('_', ' ')

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # parse HTML
        """
        page = response.url.split('/')[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)"""

        # extract data such as author, quote, and tags
        # test author argument:
        for quote in response.css('div.quote'):
            if quote.css('small.author::text').get() == self.author:
                yield {
                    'text': quote.css('span.text::text').get(),
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tags::text').getall(),
                }
        
        # How to scrape next link or page
        # 1. Using request
        """
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page) # main_url + next_page_url
            yield scrapy.Request(next_page, callback=self.parse)"""
        
        # 2. use response.follow
        """
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)"""

        # 3. same as 2, but with iterating the link
        """
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)"""
        # 3a. same as 3, but response.follow automate get href attribute from tag a
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)