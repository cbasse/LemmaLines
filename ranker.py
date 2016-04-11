import sys
import re
import math
import json

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

song_title_dict = json.load(open('Data/' + 'index/songs-title-dict'), 'utf-8')
inverse_index = json.load(open('Data/' + 'index/songs-tfidf'), 'utf-8')

query_string = sys.argv[1]
cosine_val = None
if query_string == '-song':
	song = sys.argv[2]
	for song_id, title in song_title_dict.iteritems():
		if title.lower() == song.lower():
			doc_vectors = json.load(open('Data/' + 'index/songs-doc-vector'), 'utf-8')
			cosine_val = query_cosine(doc_vectors[song_id],inverse_index,song_title_dict)
	if cosine_val == None:
		print 'song not found'
		sys.exit(0)
else:
	query_index = query_tfidf(query_string)
	cosine_val = query_cosine(query_index, inverse_index, song_title_dict)

#print out top five results
print '\n'
for x in range(0,5):
	max_doc = ''
	max_val = 0
	max_id = 0
	for song_id,val in cosine_val.iteritems():
		if max_val <= val:
			max_val = val
			max_id = song_id
	print '{}. {} - {}'.format(x+1, song_title_dict[max_id],max_val)
	cosine_val.pop(max_id, None)
	if len(cosine_val) == 0: break
print '\n'




