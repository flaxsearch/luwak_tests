import sys
import os.path
import requests
import gzip
from scrapy.selector import Selector


RANDOM_URL = 'http://en.wikipedia.org/wiki/Special:Random'
MIN_TEXT_LEN = 1000
DOWNLOAD_DIR = './text'


if __name__ == '__main__':
    for i in xrange(int(sys.argv[1])):
        text = ''
        while len(text) < MIN_TEXT_LEN:
            response = requests.get(RANDOM_URL)
            assert response.status_code == 200
            s = Selector(text=response.content)
            text = ''.join(s.xpath('//body//p//text()').extract())
        
        name = response.url.split('/')[-1]
        with gzip.open(os.path.join(DOWNLOAD_DIR, name + '.gz'), 'w') as f:
            f.write(text.encode('utf8'))

        print i, name
