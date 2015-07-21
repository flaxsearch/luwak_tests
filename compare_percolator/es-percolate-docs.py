import sys
import os
import time
import requests
import gzip
import json
import conf


if __name__ == '__main__':
    total = 0
    count = 0
    t0 = time.time()
    for fname in os.listdir(sys.argv[1]):
        if fname.endswith('.gz'):
            with gzip.open(os.path.join(sys.argv[1], fname)) as f:
                response = requests.post(conf.ES_URL + '/test/_percolate', 
                    data=json.dumps({'doc': {'text': f.read()}}))
                assert response.status_code == 200
                total += response.json()['total']
                count += 1

                print fname, response.json()['total']

#                 query_ids = [x['_id'] for x in response.json()['matches']]
#                 query_ids.sort()
#                 print '\n'.join(query_ids)
    
    t1 = time.time()
    print 'matched {0} queries for {1} documents in {2:.2f}s ({3:.2f} docs/s)'.format(
        total, count, t1-t0, count / (t1-t0))

