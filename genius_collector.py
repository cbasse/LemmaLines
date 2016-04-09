import requests
import sys
import signal
import json
import os.path
import io
import time


token = "Bearer 8ww41zHR7OoMbuHtQMKlK_6Qsx4qDNo2DmW9DE9AN8ufvPBL0fs9lP7C4-0VmlJJ"

filename = sys.argv[1]
f = None

def findLastId():
	d = json.load(open('Data/' + filename), 'utf-8')
	return d[-1]['id']

def signal_handler(signal, frame):
	time.sleep(1)
	f.close()
    	with io.open('Data/' + filename, 'r+b') as file:
	    	file.seek(-1,2)
	    	a = file.read()
	    	if a != ',':
	    		print 'something real bad happened, scoob'
	    	else:
	    		file.seek(-1,2)
	    		file.truncate()
	    		file.write(']')
	    		file.close()
	print 'gj bye'
    	sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
startId = 1;

if os.path.isfile('Data/' + filename):
	lastChar = open('Data/' + filename, 'r').read()[-1:]
	if lastChar == ']':
		startId = findLastId() + 1
		with io.open('Data/' + filename, 'r+b') as file:
			file.seek(-1, 2)
			file.truncate()
			file.write(',')
			file.close()
	elif lastChar == '':
		with io.open('Data/' + filename, 'w') as file:
			file.write(u'[')
			file.close()
	else:
		raise Exception('something real bad happened')

f = open('Data/' + filename, 'a')
for x in range(startId,1000000):
	response = requests.get("https://api.genius.com/" + filename + "/" + str(x), headers={"Authorization":token}, params={"text_format":"plain"})
	print response.json()['meta']['status']
	if response.json()['meta']['status'] == 200:
		json.dump(response.json()['response'][filename[0:-1]], f)
		f.write(u',')
	print x

f.close();

