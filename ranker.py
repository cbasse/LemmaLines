import sys
import re
import math
import simplejson as json
import requests
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

def pyongs_calc(doc_pyongs, max_pyongs):
	if doc_pyongs == None or doc_pyongs == 0:
		return 0

	return math.log10(float(doc_pyongs))/math.log10(float(max_pyongs))

def query_cosine(query_index, inverse_index, song_title_dict, exclude):
	#capture the cosine values of each document to the query
	#formula: dot-product between normalized doc and query vectors
	cosine_vals = {}
	for term, query_score in query_index.iteritems():
		for doc_id,content in song_title_dict.iteritems():
			if content['char_length'] < 500:
				continue
			if content['artist_name'] in exclude:
				continue 
			if inverse_index.has_key(term) and inverse_index[term].has_key(str(doc_id)):
				if not cosine_vals.has_key(doc_id):
					cosine_vals.update({doc_id:0})

				#formula: dot-product between normalized doc and query vectors
				cosine_vals[doc_id] += query_score * inverse_index[term][str(doc_id)]


	return cosine_vals


def query_synonyms(query_index):
	additional = {}
	for w,_ in query_index.iteritems():
		response = requests.get('https://wordsapiv1.p.mashape.com/words/'+w+'/synonyms', headers={'Accept':'application/json','X-Mashape-Key': 'lcAJdlrT9UmshBve6YoWHHURX9vCp1MyChHjsnisQgZ6o5Q3cv'})
		if response.status_code == 200:
			response = response.json()
			for syn in response['synonyms']:
				additional.update({syn:1})
	query_index.update(additional)
	return query_index
	

def query_tfidf(query_string):
	query_index = {}
	words = re.findall('[a-z]{3,}', query_string)
	for w in words:
		if query_index.has_key(w):
			query_index[w] += 1
		else:
			query_index.update({w:1})

	query_index = query_synonyms(query_index)
	#Calculate TFIDF score for each value in query inverse
	#formula: (1+log(tf))*log(N/df) 
	query_vector_length = 0
	with open('Data/index/songs-doc_freq', 'r') as file:
		doc_freq = json.load(file)
		file.close()
		for term, score in query_index.iteritems():
			#formula: (1+log(tf))*log(N/df)
			if not doc_freq.has_key(term):
				continue
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
		max_id = -1
		for song_id,val in cosine_vals.iteritems():
			if max_val <= val:
				max_val = val
				max_id = song_id
		if max_id == -1:
			break
		pyongs = 0.1 * pyongs_calc(title_dict[max_id]['pyongs_count'],793)
		views = 0.05 * pyongs_calc(title_dict[max_id]['pageviews'],2134046)
		#print title_dict[max_id]
		print '\n{}. "{}" by {} - {} cos: {} pyo: {} views: {}'.format(x+1, title_dict[max_id]['title'], title_dict[max_id]['artist_name'],max_val, max_val - pyongs - views, pyongs, views)
		cosine_vals.pop(max_id, None)
		if len(cosine_vals) == 0: break
	
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
		#set result content to highest matched keywords
		else:
			count = 0
			for ch in title_dict[max_id]['annotations']:
				if ch == '?' or ch == ' ':
					count += 1
				else:
					break
			title_dict[max_id]['annotations'] = title_dict[max_id]['annotations'][count:]
			results.append(title_dict[max_id])
		cosine_vals.pop(max_id, None)
		if len(cosine_vals) == 0: break

	return results


def ranker(query_domain,query_type,query_string):

	if query_domain == 'song':
		#song_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
		#inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')
		cosine_val = None
		if query_type == 'match':
			song = query_string
			for song_id, content in songs_title_dict.iteritems():
				if content['title'].lower() == song.lower():
					exclude = [content['artist_name']]#exclude any songs by the same artist
					cosine_val = query_cosine(songs_doc_vectors[song_id],songs_inverse_index,songs_title_dict, exclude)
			if cosine_val == None:
				print 'song not found'
				sys.exit(0)
		else:
			query_index = query_tfidf(query_string)
			cosine_val = query_cosine(query_index, songs_inverse_index, songs_title_dict, [])
		
		#printTopResults(cosine_val, songs_title_dict, 10)
		return jsonTopResults(cosine_val, songs_title_dict, 20)
	elif query_domain == 'album':
		#albums_title_dict = json.load(open('Data/' + 'index/albums-title-dict'), 'utf-8')
		#inverse_index = json.load(open('Data/' + 'index/albums-tfidf'), 'utf-8')
		cosine_val = None
		if query_type == 'match':
			album = query_string
			for album_id, content in albums_title_dict.iteritems():
				if content['title'].lower() == album.lower():
					exclude = [content['artist_name']]
					#doc_vectors = json.load(open('Data/' + 'index/albums-doc-vector'), 'utf-8')
					cosine_val = query_cosine(albums_doc_vectors[str(album_id)],albums_inverse_index,albums_title_dict,exclude)
			if cosine_val == None:
				print 'album not found'
				sys.exit(0)
		else:
			query_index = query_tfidf(query_string)
			cosine_val = query_cosine(query_index, albums_inverse_index, albums_title_dict,[])
		#printTopResults(cosine_val, albums_title_dict, 20)
		return jsonTopResults(cosine_val, albums_title_dict, 20)
	elif query_domain == 'artist':
		#albums_title_dict = json.load(open('Data/' + 'index/albums-title-dict'), 'utf-8')
		#inverse_index = json.load(open('Data/' + 'index/albums-tfidf'), 'utf-8')
		cosine_val = None
		if query_type == 'match':
			artist = query_string
			for artist_id, content in artists_title_dict.iteritems():
				if content['title'].lower() == artist.lower():
					exclude = [content['artist_name']]
					#doc_vectors = json.load(open('Data/' + 'index/albums-doc-vector'), 'utf-8')
					cosine_val = query_cosine(artists_doc_vectors[str(artist_id)],artists_inverse_index,artists_title_dict,exclude)
			if cosine_val == None:
				print 'album not found'
				sys.exit(0)
		else:
			query_index = query_tfidf(query_string)
			cosine_val = query_cosine(query_index, artists_inverse_index, artists_title_dict,[])
		#printTopResults(cosine_val, artists_title_dict, 20)
		return jsonTopResults(cosine_val, artists_title_dict, 20)

if (__name__ == '__main__'):
	songs_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
	songs_inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')
	songs_doc_vectors = json.load(open('Data/' + 'index/songs-doc-vector'), 'utf-8')

	albums_title_dict = json.load(open('Data/' + 'index/albums-title-dict'), 'utf-8')
	albums_inverse_index = json.load(open('Data/' + 'index/albums-tfidf'), 'utf-8')
	albums_doc_vectors = json.load(open('Data/' + 'index/albums-doc-vector'), 'utf-8')

	artists_title_dict = json.load(open('Data/' + 'index/artists-title-dict'), 'utf-8')
	artists_inverse_index = json.load(open('Data/' + 'index/artists-tfidf'), 'utf-8')
	artists_doc_vectors = json.load(open('Data/' + 'index/artists-doc-vector'), 'utf-8')
	print 1 
	ranker('artist','find','death')
	


