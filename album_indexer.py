import os
import json
import re
import math

def get_raw_albums():
	raw_albums = {}
	raw_songs = []

	directory_in = 'Data/songs_raw'

	for filename in os.listdir(directory_in):
		if filename[:5] != 'songs':
			continue
		raw_songs += json.load(open(directory_in + '/' + filename), 'UTF-8')


	count = 0
	for raw_song in raw_songs:
		if raw_song['album'] != None:
			album_id = raw_song['album']['id']
			count += 1
			if raw_albums.has_key(album_id):
				annotations = raw_albums[album_id]['annotations']
				raw_albums[album_id]['annotations'] = annotations + ' ' + raw_song['annotations']
				raw_albums[album_id]['num_songs'] += 1
				if raw_song['pyongs_count'] != None:
					raw_albums[album_id]['pyongs_count'] += raw_song['pyongs_count']
			else:
				raw_albums.update({album_id:{}})
				raw_albums[album_id].update({'annotations':raw_song['annotations']})
				raw_albums[album_id].update({'album': raw_song['album']})
				raw_albums[album_id].update({'num_songs':1})
				if raw_song['pyongs_count'] != None:
					raw_albums[album_id].update({'pyongs_count':raw_song['pyongs_count']})
				else:
					raw_albums[album_id].update({'pyongs_count':0})

	json.dump(raw_albums,open('Data/albums_raw/albums','w'))


#writes normalized tfidf scores to filename
def tfidf(directory_in, filename_out):
	#tokenize docs, each token as an alphebetic character sequence >=3
	num_docs = 0 
	id_title_dict = {}
	inverse_index = {}
	doc_freq = {}
	
	docs = json.load(open(directory_in,'r'), 'utf-8')
	for doc_id,content in docs.iteritems():
		id_title_dict.update({doc_id:content['album']['name']})
	num_docs += len(docs)
	for doc_id,content in docs.iteritems():
		name = doc_id
		text = content['annotations'].lower()
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

	json.dump(id_title_dict,open('Data/' + filename_out + '-title-dict', 'w'))

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
		inverse_index[term] = {doc:float(score)/doc_vector_lengths[doc] for doc, score in entries.iteritems()}
	print inverse_index[term]
	f = open('Data/' + filename_out + '-tfidf', 'w')
	json.dump(inverse_index, f)
	f = open('Data/' + filename_out + '-doc_freq', 'w')
	doc_freq.update({'n_docs':num_docs})
	json.dump(doc_freq, f)

	doc_vector = {}
	for term, data in inverse_index.iteritems():
		for doc, score in data.iteritems():
			if not doc_vector.has_key(doc):
				doc_vector.update({doc:{}})
			doc_vector[doc].update({term:score})
	json.dump(doc_vector, open('Data/' + filename_out + '-doc-vector', 'w'))

tfidf('Data/albums_raw/albums', 'index/albums')



