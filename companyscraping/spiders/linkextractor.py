import csv
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from pkg_resources import resource_filename
import tldextract

COMPANY_FILE = "resources/fhai_company_urls.csv"


class LinkSpider(Spider):
    name = "link-extractor"

    custom_settings = {
        'DEPTH_LIMIT': 2,
        'DEPTH_PRIORITY': 1
    }

    def start_requests(self):
        requests = []
        with open(resource_filename('companyscraping', COMPANY_FILE), 'rt') as csvfile:
            for row in csv.DictReader(csvfile):
                row['seed'] = True
                requests.append(Request(url=row['website'], meta=row, callback=self.parse_link_canonical))
        return requests

    def parse_link_canonical(self, response):
        canonical = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        yield { 'url': response.url,
                'canonical': canonical }

    def parse(self, response):
        if response.meta['seed']:
            yield self._create_item(response.meta, response.url)

        for link in self.links_from_domain(response):
            yield self._create_item(response.meta, link.url, link.text)
            yield Request(url=link.url, meta=response.meta, callback=self.parse)

    def links_from_domain(self, response):
        domain = '.'.join(tldextract.extract(response.url)[-2:])
        return LinkExtractor(allow=[domain]).extract_links(response)

    def _create_item(self, meta, url, text=''):
        meta['seed'] = False
        return {
            'orb_num': meta['orb_num'],
            'company': meta['name'],
            'url': url.strip(),
            'text': text.strip()
        }
