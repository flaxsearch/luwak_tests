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

def makeBoolQuery(docs):
    # get the must terms from one document so we have at least one match
    must_terms = set()
    while len(must_terms) < args.MUST:
        must_terms = set(random.choice(docs))
        
    must_terms = list(must_terms)
    random.shuffle(must_terms)
    must_terms = must_terms[:args.MUST]
        
    # get the not words from different docs
    not_terms = set()
    while len(not_terms) < args.NOT:
        not_terms.add(random.choice([x for x in random.choice(docs) if x not in conf.STOPWORDS]))

    return ' '.join(['+' + x for x in must_terms] + ['-' + x for x in not_terms])

def makeWithinQuery(docs):
    # pick two terms within the specified interval
    slop = random.randint(0, args.within)
    while True:
        doc = random.choice(docs)
        if len(doc) > slop:
            i = random.randint(0, len(doc) - slop - 1)
            if doc[i] not in conf.STOPWORDS and doc[i + slop] not in conf.STOPWORDS:
                return '"{0} {1}"~{2}'.format(doc[i], doc[i + slop], args.within)

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
    parser.add_argument('--wild', type=int, default=None,
        help='prefix length for wildcard terms')
    parser.add_argument('--within', type=int, default=None,
        help='generate a two-term phrase query with specified slop')
    
    args = parser.parse_args()
    docs = readDocs(args.docdir)
    for i in xrange(args.count):
        if i and i % 1000 == 0: print i
        with open(os.path.join(args.querydir, '{0:06d}.txt'.format(i)), 'w') as f:
            if args.within:
                f.write(makeWithinQuery(docs))
            else:
                f.write(makeBoolQuery(docs))

