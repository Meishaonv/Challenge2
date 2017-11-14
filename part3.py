import json, time, sqlite3, sys
from collections import Counter

# We have to upper the recursion limit, as the default is 1000 and the longest depth of a comment is over 1000
sys.setrecursionlimit(2000)

t0 = time.time()
cnt = 0

# Create a connection to the database
db = sqlite3.connect('reddit.db')
db.text_factory = str
c = db.cursor()
t = ('ALFKI',)

depth_dict = { }

# A function used recursivly to find the depeest comment of each top comment
# Returns the length of the deepest comment of a top comment
def searchDown(parentId, depth):
    mostDepth = 0
    
    # Selects every comment under a comment
    c.execute("SELECT id FROM comments WHERE parent_id ='%s'" % parentId)
    data = c.fetchall()
    
    # Goes through every comment
    for line in data:
        if(line[0] != parentId):
            # Goes recursivly down the comment tree
            lineDepth = searchDown(line[0],depth)
            # Saves the most depth of each branch
            if(lineDepth > mostDepth):
                mostDepth = lineDepth
        
    return mostDepth + 1

# Finds all top comments that starts with t3 as they are directly under the link
c.execute("SELECT id,subreddit_id,parent_id FROM comments WHERE parent_id like 't3%'")
topComments = c.fetchall()

for row in topComments:
    commentId = row[0]
    subreddit = row[1] #subredditId
    depth = -1 # Starts at -1, if it finds no comment under it, it   
    cnt += 1
    
    # We get the depth of each top comment
    depth = searchDown(commentId, depth)
    
    # We add the depth as a list to the relevant dictionary key
    try:
        depth_dict[subreddit].extend([depth])
    except KeyError as e:
        depth_dict[subreddit] = [depth]
        
    if (cnt % 100000 == 0):
        print cnt
        t1 = time.time()
        print t1-t0

length_count = { }

# We run through every subreddit and we calculate the average length of the comment depth
for wordSet in depth_dict:
    # Finds the name of the subreddit id
    c.execute("SELECT name FROM subreddits WHERE id ='%s'" % wordSet)
    subredditName = c.fetchone()
    # Calculates the sum of a list [2,3,4,5,6] = 20 and divides it with the length of the array
    length_count[subredditName] = sum(depth_dict[wordSet]) / float(len(depth_dict[wordSet]))

# Using the counter we can find the 10 largest values of the dictionary
C = Counter(length_count)    

print C.most_common(10)