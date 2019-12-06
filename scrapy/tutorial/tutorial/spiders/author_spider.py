import scrapy

class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com']

    def parse_author(self, response):
        def extract_css(query):
            return response.css(query).get(default='').strip()
        
        yield {
            'name': extract_css('h3.author-title::text'),
            'birthdate': extract_css('.author-born-date::text'),
            'bio': extract_css('.author-description'),
        }

    def parse(self, response):
        # parse link of author
        for href in response.css('.author + a::attr(href)'): # tag <span class="author"></span> + <a href='[link]'></a>
            yield response.follow(href, callback=self.parse_author)

        # parse link of pagination
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)