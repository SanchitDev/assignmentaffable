#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from elasticsearch import Elasticsearch, helpers
from datetime import datetime as dt


es = Elasticsearch(hosts=["10.131.73.149:9200"])

def generator():
    for pk in range(1000000, 1999999):
        resp = requests.get('http://localhost:3000/api/v1/influencers/%s'%(pk)).json()
        resp['created'] = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        yield {
                '_op_type': 'index',
                '_index': 'demo',
                '_type': 'demo',
                '_source': resp
                }
    
while True:
    #helpers.bulk(es, action,index="demo", doc_type="demo")
    #helpers.streaming_bulk(es, action, chunk_size=5000,index="demo", doc_type="demo")
    for success, info in helpers.parallel_bulk(es, generator(), thread_count=8, chunk_size=25000, 
                                               queue_size=500):
        if not success:
            print('Doc Failed', info)
