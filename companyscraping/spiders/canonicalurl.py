import csv
from scrapy import Spider, Request
from pkg_resources import resource_filename

COMPANY_FILE = "resources/testdataseedurls.csv"


class RelCanonicalCheck(Spider):
    name = "canonical-url"

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 1
    }

    def start_requests(self):
        requests = []
        with open(resource_filename('companyscraping', COMPANY_FILE), 'rt') as csvfile:
            for row in csv.DictReader(csvfile):
                requests.append(Request(url=row['website'], callback=self.parse))
        return requests

    def parse(self, response):
        canonical = response.xpath('//link[@rel="canonical"]/@href').extract_first()
        yield {'companysite': response.url,
                'canonical': canonical}
