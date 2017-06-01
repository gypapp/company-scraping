import csv
import scrapy
from scrapy.linkextractors import LinkExtractor


class LinkSpider(scrapy.Spider):
    name = "link-extractor"

    start_urls = [
        "http://www.straine.com/"
    ]

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 1
    }

    COMPANIES = 'fhai_company_urls-head.csv'

    def __init__(self):
        super(LinkSpider, self).__init__()
        self.extractor = LinkExtractor()

    def start_requests(self):
        requests = []
        with open(LinkSpider.COMPANIES, 'rt') as csvfile:
            for row in csv.DictReader(csvfile):
                requests.append(scrapy.Request(url=row['website'], meta=row, callback=self.parse))
        return requests

    def parse(self, response):
        yield self._create_item(response.meta, response.url)
        for link in self.extractor.extract_links(response):
            yield self._create_item(response.meta, link.url, link.text)
            # make a request to the page (DEPTH_LIMIT may discard it)
            yield scrapy.Request(url=link.url, meta=response.meta, callback=self.parse)

    def _create_item(self, meta, url, text=''):
        return {
            'orb_num': meta['orb_num'],
            'company': meta['name'],
            'url': url,
            'text': text
        }