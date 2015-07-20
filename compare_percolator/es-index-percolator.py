import sys
import os
import requests
import json
import conf

if __name__ == '__main__':
    for fname in os.listdir(sys.argv[1]):
        if fname.endswith('.txt'):
            query_id = fname.split('.')[0]
            query_url = '{0}/.percolator/{1}'.format(conf.ES_URL, query_id)
            with open(os.path.join(sys.argv[1], fname)) as f:
                query_obj = { 'query': { 'query_string': {
                    'default_field': conf.DEFAULT_FIELD,
                    'query': f.read() }}}
                response = requests.put(query_url, data=json.dumps(query_obj))
                assert response.status_code == 201
                print query_url
