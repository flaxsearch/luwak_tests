import sys
import os
import requests
import conf

if __name__ == '__main__':
    for fname in os.listdir(conf.QUERY_DIR):
        if fname.endswith('.json'):
            query_id = fname.split('.')[0]
            query_url = '{0}/.percolator/{1}'.format(conf.ES_URL, query_id)
            with open(os.path.join(conf.QUERY_DIR, fname)) as f:
                response = requests.put(query_url, data=f.read())
                print query_url, response.status_code
