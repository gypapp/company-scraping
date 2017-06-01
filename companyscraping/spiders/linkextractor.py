import csv
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from pkg_resources import resource_filename


COMPANY_FILE = "resources/fhai_company_urls.csv"


class LinkSpider(Spider):
    name = "link-extractor"

    custom_settings = {
        'DEPTH_LIMIT': 2,
        'DEPTH_PRIORITY': 1
    }

    def __init__(self):
        super(LinkSpider, self).__init__()
        self.extractor = LinkExtractor()

    def start_requests(self):
        requests = []
        with open(resource_filename('companyscraping', COMPANY_FILE), 'rt') as csvfile:
            for row in csv.DictReader(csvfile):
                requests.append(Request(url=row['website'], meta=row, callback=self.parse))
        return requests

    def parse(self, response):
        # remove if you don't need the seed url
        if 'text' not in response.meta:
            yield self._create_item(response.meta, response.url)
        for link in self.extractor.extract_links(response):
            # yield all the links as a result item to pipeline
            yield self._create_item(response.meta, link.url, link.text)
            # make a request to the page (DEPTH_LIMIT may discard it)
            yield Request(url=link.url, meta=response.meta, callback=self.parse)

    def _create_item(self, meta, url, text=''):
        return {
            'orb_num': meta['orb_num'],
            'company': meta['name'],
            'url': url,
            'text': text
        }
