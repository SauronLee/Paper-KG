import scrapy


class ConfSpider(scrapy.Spider):
    name = 'conf'
    allowed_domains = ['']
    start_urls = ['http:///']

    def parse(self, response):
        pass
