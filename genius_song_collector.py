import requests
import sys

token = "Bearer 8ww41zHR7OoMbuHtQMKlK_6Qsx4qDNo2DmW9DE9AN8ufvPBL0fs9lP7C4-0VmlJJ"


filename = 'songs'
f = open('Data/'+str(filename),'a')
for x in range(int(sys.argv[1]),1000000):
	response = requests.get("https://api.genius.com/songs/" + str(x), headers={"Authorization":token}, params={"text_format":"plain"})
	print response.json()['meta']['status']
	if response.json()['meta']['status'] == 200:
		f.write('{\"id\" : \"' + str(x) + '\",\n')
		f.write('\"song\" : \"' + response.json()['response']['song']['title'].encode('utf8') + '\",\n')
		f.write('\"description\" : \"' + response.json()['response']['song']['description']['plain'].encode('utf8') + '\"},\n\n\n')
	print x
f.close();

