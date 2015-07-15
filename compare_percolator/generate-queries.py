import sys
import os
import requests
import gzip
import re
import json
import random
import conf


def readDocs(docdir):
    """ read all docs into memory, parse into lists of words
    """
    docs = []
    for fname in os.listdir(docdir):
        if fname.endswith('.gz'):
            with gzip.open(os.path.join(docdir, fname)) as f:
                docs.append([x.lower() for x in conf.WORD_RE.findall(f.read())])
    return docs

def makeBoolQuery(docs, must_count, should_count, not_count):
    must_terms = set()
    should_terms = set()
    not_terms = set()
    
    # get all the must words from one document
    d = random.choice(docs)
    while len(must_terms) < must_count:
        must_terms.add(random_nonstopword(d))
    
    # get should and not terms from separate docs
    while len(should_terms) < should_count:
        should_terms.add(random_nonstopword(random.choice(docs)))

    while len(not_terms) < not_count:
        not_terms.add(random_nonstopword(random.choice(docs)))
        
    return { 'query': { 'bool': {
        'must': [{ 'term': { conf.DEFAULT_TERM: x }} for x in must_terms],
        'should': [{ 'term': { conf.DEFAULT_TERM: x }} for x in should_terms],
        'must_not': [{ 'term': { conf.DEFAULT_TERM: x }} for x in not_terms]
    }}}

def random_nonstopword(words):
    while True:
        w = random.choice(words)
        if w not in conf.STOPWORDS:
            return w

def printMostCommonWords(docs):
    counts = {}
    for doc in docs:
        for word in doc:
            counts[word] = counts.get(word, 0) + 1
    
    counts = counts.items();
    counts.sort(cmp=lambda a, b: -1 if a[1] > b[1] else +1 if a[1] < b[1] else 0)
    for c in counts[:200]:
        print c


if __name__ == '__main__':
    docs = readDocs(conf.DOC_DIR)
    for i in xrange(int(sys.argv[1])):
        with open(os.path.join(conf.QUERY_DIR, '{0:06d}.json'.format(i)), 'w') as f:
            json.dump(makeBoolQuery(docs, 3, 3, 1), f)
