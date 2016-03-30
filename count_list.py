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
								  a != 'their' and
								  a != 'that', words)


def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

print 'top 50 words in \"' + doc + '\":'
for x in range(0,50):
	most = most_common(filtered_words)
	count = 0
	for y in filtered_words:
		if y == most:
			count += 1
	filtered_words = filter(lambda a: a != most, filtered_words)
	print str(x+1)+': \"'+most+'\", '+str(count)+' times'

