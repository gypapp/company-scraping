import scrapy
from scrapy.linkextractors import LinkExtractor


class LinkSpider(scrapy.Spider):
    name = "link-extractor"
    allow_domains = 'tiempodev.com'
    start_urls = [
        'http://www.tiempodev.com/index',
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=self.allow_domains)
        for link in extractor.extract_links(response):
            yield {
                'url': link.url,
                'text': link.text
            }
