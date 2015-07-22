import re

RANDOM_URL = 'http://en.wikipedia.org/wiki/Special:Random'
MIN_TEXT_LEN = 1000

WORD_RE = re.compile(r'\w{2,50}')
DEFAULT_FIELD = 'text'

STOPWORDS = set(['the', 'of', 'and', 'in', 'to', 'was', 'for', 'as', 'on', 'with', 'is', 
    'by', 'an', 'that', 'he', 'at', 'from', 'his', 'it', 'were', 'which', 'be', 'their', 
    'this', 'they', 'or', 'her', 'not', 'have', 'had', 'has', 'all', 'are'])

ES_URL = 'http://localhost:9200/'
ES_DB = 'test'