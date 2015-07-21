import sys
import os.path
import requests
import gzip
from scrapy.selector import Selector
import conf


if __name__ == '__main__':
    for i in xrange(int(sys.argv[1])):
        text = ''
        while len(text) < conf.MIN_TEXT_LEN:
            response = requests.get(conf.RANDOM_URL)
            assert response.status_code == 200
            s = Selector(text=response.content)
            text = ''.join(s.xpath('//body//p//text()').extract())
        
        name = response.url.split('/')[-1]
        with gzip.open(os.path.join(sys.argv[2], name + '.gz'), 'w') as f:
            f.write(text.encode('utf8'))

        print i, name
