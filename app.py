#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from flask import Flask
from flask import render_template
from flask import request
import ranker
import json


app = Flask(__name__)

#results = ranker.ranker("-song","","kanye")

ranker.song_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
ranker.inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')
ranker.doc_vectors = json.load(open('Data/' + 'index/songs-doc-vector'), 'utf-8')


@app.route("/")
def hello():
    return render_template('search.html')
    
@app.route("/getstuff")
def getstuff():
    args = request.args
    print args['query']
    return json.dumps(ranker.ranker(args['domain'],args['type'],args['query']))


#results = 
app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8080)))

