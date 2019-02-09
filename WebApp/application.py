#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, render_template
from flask_cors import CORS
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(hosts=["10.131.73.149:9200"]
)
app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/api/v1/resources/infochart")   
def chart_plot():
    
    if "username" in request.args:
        username = request.args["username"]
        query = {
	"query": {
		"bool": {
			"must": [{
					"term": {
						"username": username
					}
				},
				{
					"range": {
						"created": {
							"gte": "now-1d",
							"lt": "now"
						}
					}
				}
			]
		}
	}
}
        result = es.search(index="demo", doc_type="demo",body=json.dumps(query), 
                           size=10000,sort='created:desc')["hits"]
        values = [res["_source"]["followerCount"] for res in result["hits"]]
        labels = [res["_source"]["created"] for res in result["hits"]]
        suspicion = es.get(index="demosuspicious", doc_type="demosuspicious", id=result["hits"][0]["_source"]["pk"])
        
        return render_template('chart.html', values=values, username=username, 
                               averageFollowerCount=round(sum(values)/float(len(values)), 2), 
                               recentData=result["hits"][0]["_source"],
                               suspicious=suspicion["_source"]["suspicious"],labels=labels)
    else:
        return "UserName not specified"

if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True)