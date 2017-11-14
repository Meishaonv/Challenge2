import json, re, time
from collections import Counter
from copy import deepcopy

t0 = time.time()
cnt = 0

auth_dict = { }

# We go through every json line in the reddit file
with open('reddit.json') as f:
    for line in f:  
        try:
            cnt +=1
            jsonLine = json.loads(line)
            subreddit = jsonLine['subreddit'] # Subreddit name
            author = jsonLine['author'] # Comment text
            
            # We add the author to the relevant dictionary key
            # Each dictionary holds the set of different authors for every subreddit
            try: 
                auth_dict[subreddit].update(set([author]))
            except KeyError as e:
                auth_dict[subreddit] = set([author])  
            
            # Counter to see the progress
            if(cnt%1000000 == 0):
                print cnt
                t1 = time.time()
                print t1-t0
        except ValueError:
            print "error"
            
t0 = time.time()
cnt = 0

subredditPair_count = {}
# Creates a copy of the author dictionary key
newAuth_dict = deepcopy(auth_dict)

# We run through every subreddit
for key,value in auth_dict.iteritems():
    cnt += 1
    # We delete the current key from the copied dictionary
    try:
        del newAuth_dict[key]
    except KeyError:
        pass
    
    # Counter to see progress
    if(cnt%1000 == 0):
        print cnt 
        t1 = time.time()
        print t1-t0
        
    # We now run through all the dictionaries except the ones we have already runned trough
    # By removing the values from the copied dictionary we never make the same one twice
    for key2,value2 in newAuth_dict.iteritems():
        name = key + "," + key2 # The comparing subreddits name
        commonAuthors = value & value2 # Authors that are in both subreddits
        
        # If common author length is higher than the lowest value in the dictionary we remove
        # the lowest dictionary and add the new one in
        # That leaves us with the 10 highest subreddits
        if len(subredditPair_count) > 9:
            lowestValue = 1000000000 #High value so the lowest gets picked up
            lowestKey = ""        
            for key3,value3 in subredditPair_count.iteritems():
                if(lowestValue > value3):
                    lowestValue = value3
                    lowestKey = key3
            if(lowestValue < len(commonAuthors)): 
                try:
                    del subredditPair_count[lowestKey]
                except KeyError:
                    pass
                subredditPair_count[name] = len(commonAuthors)
            
        else:
            subredditPair_count[name] = len(commonAuthors)

t1 = time.time()

print t1-t0
print subredditPair_count