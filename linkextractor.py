import scrapy
from scrapy.linkextractors import LinkExtractor
import tldextract


class LinkSpider(scrapy.Spider):
    name = "link-extractor"
    start_urls = [
        'http://www.tiempodev.com/index',
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=self._get_domain(response.url))
        for link in extractor.extract_links(response):
            yield {
                'url': link.url,
                'text': link.text
            }

    def _get_domain(self, url):
        ext = tldextract.extract(url)
        return ext.domain + '.' + ext.suffix
