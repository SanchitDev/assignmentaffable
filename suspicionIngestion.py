#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts=["10.131.73.149:9200"])

def generator():
    for pk in range(1000000, 1999999):
        resp = requests.get('http://localhost:3000/api/v1/influencers/%s'%(pk)).json()
        resp_suspicious = requests.post('http://localhost:3000/api/v1/influencers/is_suspicious',json=resp).json()

        
        yield {
                '_op_type': 'index',
                '_index': 'demosuspicious',
                '_type': 'demosuspicious',
                '_id': resp_suspicious['pk'],
                '_source': resp_suspicious
                }
    

if __name__=="__main__":
        
    for success, info in helpers.parallel_bulk(es, generator(), thread_count=8, chunk_size=500):
        if not success:
            print('Doc Failed', info)