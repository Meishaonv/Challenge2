import json, re, time
from collections import Counter

t0 = time.time()

# Using the teacher given script to return a set of different words from a text
def differentWords(text):
    symbols = ['\n','`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[',']','}','|','\\',':',';','"',"'",'<','>','.','?','/',',']

    text = text.lower()
    for sym in symbols:
        text = text.replace(sym, " ")

    words = set()
    for w in text.split(" "):
        if len(w.replace(" ","")) > 0:
            words.add(w)

    return words

word_dict = { }

cnt = 0

# We go through every json line in the reddit file
with open('reddit.json') as f:
    for line in f:  
        try:
            cnt +=1
            jsonLine = json.loads(line)
            subreddit = jsonLine['subreddit'] # Subreddit name
            body = jsonLine['body'] # Comment text
            setOfWords = differentWords(body) # Set of a different words in the comment text
            
            # We add the set to the relevant dictionary key
            # Each dictionary holds the set of different words for every subreddit
            try:
                word_dict[subreddit].update(setOfWords)
            except KeyError as e:
                word_dict[subreddit] = setOfWords
                
            if(cnt%1000000 == 0):
                print cnt
                t1 = time.time()
                print t1-t0
                
        except ValueError:
            print "error"
            
t1 = time.time()

print t1-t0

subreddit_count = {}

# Fills the new dictionary with the length of different words in each subreddit
for wordSet in word_dict:
    subreddit_count[wordSet] = len(word_dict[wordSet])

# Using the counter we can find the 10 highest values of the dictionary
C = Counter(subreddit_count)    

print C.most_common(10)