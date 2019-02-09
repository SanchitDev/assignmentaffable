#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from elasticsearch import Elasticsearch, helpers
from datetime import datetime as dt


es = Elasticsearch(hosts=["10.131.73.149:9200"])

def generator():
    for pk in range(1000000, 1250000):
        resp = requests.get('http://localhost:3000/api/v1/influencers/%s'%(pk)).json()
        time_s = dt.strptime(str(dt.utcnow()),'%Y-%m-%d %H:%M:%S.%f')
        resp['created'] = (str(format(time_s.date()))+ " " + str(format(time_s.hour, '02d')) + ':'  + str(format(time_s.minute, '02d') + ':' + str(format(time_s.second, '02d'))))
        resp['followerRatio'] = round(resp['followerCount']/resp['followingCount'], 2)
        yield {
                '_op_type': 'index',
                '_index': 'demo',
                '_type': 'demo',
                '_source': resp
                }
    
while True:
    
    for success, info in helpers.parallel_bulk(es, generator(), thread_count=4, chunk_size=5000, 
                                               queue_size=500):
        if not success:
            print('Doc Failed', info)
