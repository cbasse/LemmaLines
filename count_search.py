import re
import sys
import ast
import itertools
import operator

doc = sys.argv[1]
query = sys.argv[2]

text = open('Data' + '/' + doc).read().lower()
words = re.findall('[a-z]{3,}', text)
filtered_words = filter(lambda a: a != 'description' and 
								  a != 'artist' and
								  a != 'the' and
								  a != 'and' and
								  a != 'his' and
								  a != 'with' and
								  a != 'for' and
								  a != 'was' and
								  a != 'from' and
								  a != 'has' and
								  a != 'that' and
								  a != 'their', words)

count = 0
for x in filtered_words:
	if x == query:
		count += 1

print '\nthe word \"' + query + '\" appears ' + str(count) + ' times in \"' + doc + '\"!\n'