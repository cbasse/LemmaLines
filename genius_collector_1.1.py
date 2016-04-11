import requests
import sys
import signal
import json
import os.path
import io
import time


token = "Bearer 8ww41zHR7OoMbuHtQMKlK_6Qsx4qDNo2DmW9DE9AN8ufvPBL0fs9lP7C4-0VmlJJ"

filename = sys.argv[1]
filenumber = int(sys.argv[2])
f = None

def find_last_id():
	d = json.load(open('Data/' + filename + str(filenumber)), 'utf-8')
	return d[-1]['song_id']

def close_file():
	time.sleep(1)
	f.close()
    	with io.open('Data/' + filename + str(filenumber), 'r+b') as file:
	    	file.seek(-1,2)
	    	a = file.read()
	    	if a != ',':
	    		print 'something real bad happened, scoob'
	    	else:
	    		file.seek(-1,2)
	    		file.truncate()
	    		file.write(']')
	    		file.close()

def signal_handler(signal, frame):
	close_file()
	print '\ngj bye'
	sys.exit(0)

def get_annotations(page, x):
	response = requests.get("https://api.genius.com/" + 'referents', headers={"Authorization":token}, params={"text_format":"plain","song_id":str(x),"per_page":"50","page":str(page)})
	response = response.json()
	annotations = ''
	for ref in response['response']['referents']:
		for annotation in ref['annotations']:
			annotations += annotation['body']['plain'] + u' '
	
	if len(response['response']['referents']) == 50:
		annotations += get_annotations(page+1, x)

	return annotations

signal.signal(signal.SIGINT, signal_handler)
startId = 1;

if os.path.isfile('Data/' + filename + str(filenumber)):
	lastChar = open('Data/' + filename + str(filenumber), 'r').read()[-1:]
	if lastChar == ']':
		startId = find_last_id() + 1
		with io.open('Data/' + filename + str(filenumber), 'r+b') as file:
			file.seek(-1, 2)
			file.truncate()
			file.write(',')
			file.close()
	elif lastChar == '':
		with io.open('Data/' + filename + str(filenumber), 'w') as file:
			file.write(u'[')
			file.close()
	else:
		raise Exception('something real bad happened')

f = open('Data/' + filename + str(filenumber), 'a')
for x in range(startId,1000000):
	if x % 1000 == 0:
		close_file()
		filenumber += 1
		f = open('Data/' + filename + str(filenumber), 'a')
		f.write('[')

	response = requests.get("https://api.genius.com/" + 'songs' + "/" + str(x), headers={"Authorization":token}, params={"text_format":"plain"})
	response = response.json()
	print response['meta']['status']
	annotations = ''
	temp = {}
	if response['meta']['status'] == 200:
		temp.update({u'song_id':x})
		temp.update({u'title':response['response']['song']['title']})
		temp.update({u'pyongs_count':response['response']['song']['pyongs_count']})
		temp.update({u'stats':response['response']['song']['stats']})
		temp.update({u'artist':response['response']['song']['primary_artist']})
		temp.update({u'album':response['response']['song']['album']})
		
		annotations = response['response']['song']['description']['plain'] + u' '

		annotations += get_annotations(1, x)

		temp.update({u'annotations':annotations})
		
		json.dump(temp,f)
		f.write(u',')
	print x

f.close();

