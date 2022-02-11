import scrapy


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['http://superjob.ru/']

    def parse(self, response):
        pass
