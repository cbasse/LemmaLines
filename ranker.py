import sys
import re
import math
import simplejson as json

import gzip
import cStringIO

def decompressFiletoJson(inputFile):
  """
  decompress the given string value (which must be valid compressed gzip
  data) and write the result in the given open file.
  """
  jsonString = ""
  stream = cStringIO.StringIO(inputFile.read())
  decompressor = gzip.GzipFile(fileobj=stream, mode='r')
  while True:  # until EOF
    chunk = decompressor.read(8192)
    if not chunk:
      decompressor.close()
      print -1
      return json.loads(jsonString, 'utf-8')
    jsonString += chunk

def query_cosine(query_index, inverse_index, song_title_dict):
	#capture the cosine values of each document to the query
	#formula: dot-product between normalized doc and query vectors
	cosine_vals = {}
	for term, query_score in query_index.iteritems():
		for doc_id,_ in song_title_dict.iteritems():
			if inverse_index.has_key(term) and inverse_index[term].has_key(str(doc_id)):
				if not cosine_vals.has_key(doc_id):
					cosine_vals.update({doc_id:0})
				#formula: dot-product between normalized doc and query vectors
				cosine_vals[doc_id] += query_score * inverse_index[term][str(doc_id)]

	return cosine_vals

def query_tfidf(query_string):
	query_index = {}
	words = re.findall('[a-z]{3,}', query_string)
	for w in words:
		if query_index.has_key(w):
			query_index[w] += 1
		else:
			query_index.update({w:1})


	#Calculate TFIDF score for each value in query inverse
	#formula: (1+log(tf))*log(N/df) 
	query_vector_length = 0
	with open('Data/index/songs-doc_freq', 'r') as file:
		doc_freq = json.load(file)
		file.close()
		for term, score in query_index.iteritems():
			#formula: (1+log(tf))*log(N/df)
			new_val = (1+math.log10(score))*(math.log10(float(doc_freq['n_docs'])/doc_freq[term]))
			query_vector_length += math.pow(new_val,2.0)
			query_index[term] = new_val


	#Get doc vector lengths
	#formula: sqrt(a2 + b2 + c2 ...)
	query_vector_length = math.sqrt(float(query_vector_length))

	#normalize tfidf scores
	query_index = {term: score/query_vector_length for term, score in query_index.iteritems()}

	return query_index

def printTopResults(cosine_vals, title_dict, top):
	results = ''
	for x in range(0,top):
		max_doc = ''
		max_val = 0
		max_id = 0
		for song_id,val in cosine_vals.iteritems():
			if max_val <= val:
				max_val = val
				max_id = song_id
		results += '\n{}. {} - {}'.format(x+1, title_dict[max_id],max_val)
		cosine_vals.pop(max_id, None)
		if len(cosine_vals) == 0: break
	return results
	
def jsonTopResults(cosine_vals, title_dict, top):
	results = []
	for x in range(0,top):
		max_doc = ''
		max_val = 0
		max_id = -1
		for song_id,val in cosine_vals.iteritems():
			if max_val <= val:
				max_val = val
				max_id = song_id
		if max_id == -1:
			break
		print title_dict[max_id]
		results.append(title_dict[max_id])
		cosine_vals.pop(max_id, None)
		if len(cosine_vals) == 0: break
	return results
	
songs_title_dict = None
songs_inverse_index = None
songs_doc_vectors = None

albums_title_dict = None
albums_inverse_index = None
albums_doc_vectors = None



def ranker(query_domain,query_type,query_string):

	if query_domain == 'song':
		#song_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
		#inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')
		cosine_val = None
		if query_type == 'match':
			song = query_string
			for song_id, content in songs_title_dict.iteritems():
				if content['title'].lower() == song.lower():
					#doc_vectors = json.load(open('Data/' + 'index/songs-doc-vector'), 'utf-8')
					print songs_doc_vectors[song_id]
					cosine_val = query_cosine(songs_doc_vectors[song_id],songs_inverse_index,songs_title_dict)
			if cosine_val == None:
				print 'song not found'
				sys.exit(0)
		else:
			query_index = query_tfidf(query_string)
			cosine_val = query_cosine(query_index, albums_inverse_index, songs_title_dict)
		return jsonTopResults(cosine_val, songs_title_dict, 20)
	elif query_domain == 'album':
		#albums_title_dict = json.load(open('Data/' + 'index/albums-title-dict'), 'utf-8')
		#inverse_index = json.load(open('Data/' + 'index/albums-tfidf'), 'utf-8')
		cosine_val = None
		if query_type == 'match':
			album = query_string
			for album_id, content in albums_title_dict.iteritems():
				if content['title'].lower() == album.lower():
					#doc_vectors = json.load(open('Data/' + 'index/albums-doc-vector'), 'utf-8')
					cosine_val = query_cosine(albums_doc_vectors[str(album_id)],albums_inverse_index,albums_title_dict)
			if cosine_val == None:
				print 'album not found'
				sys.exit(0)
		else:
			query_index = query_tfidf(query_string)
			cosine_val = query_cosine(query_index, albums_inverse_index, albums_title_dict)
		return jsonTopResults(cosine_val, albums_title_dict, 20)

if (__name__ == '__main__'):
	songs_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
	songs_inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')
	songs_doc_vectors = json.load(open('Data/' + 'index/songs-doc-vector'), 'utf-8')

	albums_title_dict = json.load(open('Data/' + 'index/albums-title-dict'), 'utf-8')
	albums_inverse_index = json.load(open('Data/' + 'index/albums-tfidf'), 'utf-8')
	albums_doc_vectors = json.load(open('Data/' + 'index/albums-doc-vector'), 'utf-8')
	ranker('song','find','hello world')
	print 1
	ranker('song','match','harder')
	print 2
	ranker('album','find','hello world')
	print 3
	ranker('album','match','watch the throne')


