#!/usr/bin/python
import os
import re
import sys
import math
import random
import json

import gzip
import cStringIO

def compressFileToString(inputFile):
  """
  read the given open file, compress the data and return it as string.
  """
  stream = cStringIO.StringIO()
  compressor = gzip.GzipFile(fileobj=stream, mode='w')
  while True:  # until EOF
    chunk = inputFile.read(8192)
    if not chunk:  # EOF?
      compressor.close()
      return open("testzip","w").write(stream.getvalue())
    compressor.write(chunk)

#writes normalized tfidf scores to filename
def tfidf(directory_in, filename_out):
	#tokenize docs, each token as an alphebetic character sequence >=3
	num_docs = 0 
	song_title_dict = {}
	inverse_index = {}
	doc_freq = {}
	doc_vector = {}
	
	
	for filename in os.listdir(directory_in):
		print filename 
		if filename[:5] != 'songs':
			continue
		docs = json.load(open(directory_in + '/' + filename,'r'), 'utf-8')
		for doc in docs:
			song_id = int(doc['song_id'])
			song_title_dict.update({song_id:{}})
			song_title_dict[song_id].update({'title':doc['title']})
			song_title_dict[song_id].update({'url':'http://genius.com/songs/'+str(song_id)})
			song_title_dict[song_id].update({'pyongs_count':doc['pyongs_count']})
			song_title_dict[song_id].update({'artist_name':doc['artist']['name']})
			song_title_dict[song_id].update({'artist_url':doc['artist']['url']})
			song_title_dict[song_id].update({'char_length':len(doc['annotations'])})
			song_title_dict[song_id].update({'annotations':doc['annotations'][:250] + '...'})
			if not doc['stats'].has_key('pageviews'):
				song_title_dict[song_id].update({'pageviews':0})
			else:
				song_title_dict[song_id].update({'pageviews':doc['stats']['pageviews']})
			doc_vector.update({song_id:{}})

		num_docs += len(docs)
		for doc in docs:
			name = doc['song_id']
			text = doc['annotations'].lower()
			text += ' ' + doc['title'].lower() 
			words = re.findall('[a-z]{3,}', text)
			for w in words:
				if inverse_index.has_key(w) and inverse_index[w].has_key(name):
					inverse_index[w][name] += 1
				elif inverse_index.has_key(w):
					inverse_index[w].update({name:1})
					doc_freq[w] += 1
				else:
					inverse_index.update({w:{name:1}})
					doc_freq.update({w:1})

	json.dump(song_title_dict,open('Data/' + filename_out + '-title-dict', 'w'))

	#Calculate TFIDF score for each value in doc inverse index
	#formula: (1+log(tf))*log(N/df) 
	doc_vector_lengths = {}
	for term in inverse_index.iteritems():
		for entry in term[1].iteritems():
			#formula: (1+log(tf))*log(N/df) 
			new_val = (1+math.log10(entry[1]))*(math.log10(float(num_docs)/doc_freq[term[0]]))
			if not doc_vector_lengths.has_key(entry[0]):
				doc_vector_lengths.update({entry[0]:0})
			doc_vector_lengths[entry[0]] += math.pow(new_val,2.0)
			inverse_index[term[0]][entry[0]] = new_val

	#Get doc vector lengths
	#formula: sqrt(a2 + b2 + c2 ...)
	doc_vector_lengths = {doc: math.sqrt(float(val)) for doc, val in doc_vector_lengths.iteritems()}

	#Normalize doc vectors
	#formula: (TFIDF score) / (Vector length)
	for term, entries in inverse_index.iteritems():
		inverse_index[term] = {doc:round(float(score)/doc_vector_lengths[doc],3) for doc, score in entries.iteritems()}
	f = open('Data/' + filename_out + '-tfidf', 'w')
	json.dump(inverse_index, f)
	f.close()
	#compressFileToString(open('Data/' + filename_out + '-tfidf', 'r'))
	f = open('Data/' + filename_out + '-doc_freq', 'w')
	doc_freq.update({'n_docs':num_docs})
	json.dump(doc_freq, f)
	f.close()
	
	for term, data in inverse_index.iteritems():
		for doc, score in data.iteritems():
			if not doc_vector.has_key(doc):
				doc_vector.update({doc:{}})
			doc_vector[doc].update({term:score})
	json.dump(doc_vector, open('Data/' + filename_out + '-doc-vector', 'w'))

tfidf('Data/songs_raw', 'index/songs')
