import sys
import argparse
import os
import requests
import gzip
import re
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

def makeBoolQuery(docs, must_count, not_count):
    must_terms = set()
    not_terms = set()
    
    # get all the must words from one document
    d = random.choice(docs)
    while len(must_terms) < must_count:
        must_terms.add(random_nonstopword(d))

    # and the not words from different docs    
    while len(not_terms) < not_count:
        not_terms.add(random_nonstopword(random.choice(docs)))

    return ' '.join(['+' + x for x in must_terms] + ['-' + x for x in not_terms])

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
    parser = argparse.ArgumentParser(description='Generate random queries from documents')
    parser.add_argument('--count', type=int, required=True, 
        help='number of queries to generate')
    parser.add_argument('--docdir', type=str, required=True,
        help='document directory')
    parser.add_argument('--querydir', type=str, required=True,
        help='generated query directory')
    parser.add_argument('--MUST', type=int, default=1, 
        help='number of MUST terms to include in queries')
    parser.add_argument('--NOT', type=int, default=0, 
        help='number of NOT terms to include in queries')
    
    args = parser.parse_args()
    docs = readDocs(args.docdir)
    for i in xrange(args.count):
        with open(os.path.join(args.querydir, '{0:06d}.txt'.format(i)), 'w') as f:
            f.write(makeBoolQuery(docs, args.MUST, args.NOT))

