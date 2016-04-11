# LemmaLines
Search engine that recommends music based off musical mofifs or themes. Uses annotations retrieved from the Genius API as document collection.

Clone the repository and ensure that you have the "Data" folder. That's where the document collection lives, along with the tfidf index and other helpful json objects. The core of our algorithm uses cosine similiarity with tfidf. The documents we are searching through themselves are songs on Genius with all the annotations associated with them. As of this point we've collected ~9,000 songs. We recently changed our scraper, so we had to start over in collecting the documents. 

To run:

ensure your in the current working directory that contains the "Data" folder and the "ranker.py" file.

to find songs based on a particular motif/theme:

$ python ranker.py "MOTIF HERE"

to find songs with similiar content to a particular song type:

$ python ranker.py -song "SONG HERE"
(note: this feature is still primitive, so the song title must be perfectly spelled and already exist in the collection)


EXAMPLES:

$ python ranker.py 'sad'

1. Somebody Already Broke My Heart - 0.272399255083
2. Made To Be Together - 0.187276338082
3. Let Me Buy U A Drink - 0.148157669342
4. I Wish - 0.131954907473
5. So Fly - 0.128562356066


$ python ranker.py 'money power wealth' 

1. Glitter - 0.168878862684
2. Any Girl - 0.0880240472042
3. The Name Game - 0.0807053337038
4. All of Me - 0.0797245172989
5. He Wishes for the Cloths of Heaven - 0.0736877071889


$ python ranker.py 'food puppies'

1. Martha My Dear - 0.156185290791
2. Frisky - 0.107879688286
3. I Gotcha - 0.105866861719
4. Pressure - 0.0870502742077
5. Go DJ - 0.0767641949908


$ python ranker.py -song 'martha my dear'

1. Martha My Dear - 1.0
2. Yesterday - 0.149195486126
3. Let It Be - 0.124583387816
4. Happiness Is A Warm Gun - 0.0942326257869
5. For No One - 0.0913203148984


$ python ranker.py -song 'power'

1. Power - 1.0
2. Power (Remix) - 0.19399928664
3. All of the Lights - 0.12338616064
4. Monster - 0.121312510045
5. Gorgeous - 0.117727001056


$ python ranker.py -song 'bohemian rhapsody'

1. Bohemian Rhapsody - 1.0
2. One Mic - 0.0901673839659
3. Devil In a New Dress - 0.0880562488001
4. Dance With The Devil - 0.0864832003069
5. Stairway to Heaven - 0.0864596214922








