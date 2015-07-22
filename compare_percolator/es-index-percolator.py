import sys
import os
import requests
import json
import conf

if __name__ == '__main__':
    bulk = []
    count = 0
    for fname in os.listdir(sys.argv[1]):
        if fname.endswith('.txt'):
            query_id = fname.split('.')[0]
            bulk.append('{"index":{"_index":"%s","_type":".percolator","_id":"%s"}}'
                % (conf.ES_DB, query_id))
            with open(os.path.join(sys.argv[1], fname)) as f:
                query_obj = { 'query': { 'query_string': {
                    'default_field': conf.DEFAULT_FIELD,
                    'query': f.read() }}}
                bulk.append(json.dumps(query_obj))
                if len(bulk) == 100:
                    response = requests.put(conf.ES_URL + '_bulk',
                        data='\n'.join(bulk) + '\n')
                    assert response.status_code == 200
                    count += len(bulk)
                    print count
                    bulk = []

    if bulk:
        response = requests.put(conf.ES_URL + '_bulk', data='\n'.join(bulk) + '\n')
        assert response.status_code == 200
