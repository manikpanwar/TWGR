import getUserTweets as gut 
import csv


def readCsv():
    with open('output.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='"', quotechar='|')
        i = 0
        d = dict()
        userId = -1
        genre = ""
        for row in spamreader:
            if i == 0:
                userId = int(row[1])
                i += 1
            elif i == 1:
                genre = row[1].split(",")[1]
                d[userId] = genre
                i = 0
        return d


def writeCsv(d, users = None):
    keysIterated = d.keys()
    if users != None:
        keysIterated = users
    with open('extended-output.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for userId in users:
            (genre, text) = d[userId]
            spamwriter.writerow([[userId], [genre], [text]])
    print "Made extended-output.csv"

def getTweetsMap():
    d = readCsv()
    numUsers = 100
    numWordsPerUser = 30
    users = []
    for userId in d.keys()[:numUsers]:
        val = d[userId]
        # print userId, d[userId], 
        tweets = gut.getUserTweetsByUserID(userId)
        if tweets == "":
            continue
        users += [userId]
        tweets = ".".join(tweets.split("\n"))
        t = ' '.join(tweets.split(" ")[:numWordsPerUser])
        # d[userId] = (val, (t.encode('utf-8')).encode('ascii', errors='ignore'))
        d[userId] = (val, (t).encode('ascii', errors='ignore'))
        # print ' '.join(tweets.split(" "))

    writeCsv(d, users)

getTweetsMap()

