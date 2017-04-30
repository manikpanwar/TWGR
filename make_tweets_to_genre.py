import getUserTweets as gut 
import csv
import train_test as tt

def readFile(filename, mode="rt"):
    # From 15-112 class notes
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def writeFile(filename, contents, mode="wt"):
    # From 15-112 class notes
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

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
    numUsers = 50
    numWordsPerUser = 100
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
    return d, users

    # writeCsv(d, users)

def writeToTextFile():
    d, users = getTweetsMap()
    keysIterated = d.keys()
    if users != None:
        keysIterated = users
    s = ""
    for userId in keysIterated:
        (genre, text) = d[userId]
        s += str(userId) + "\n"
        s += genre + "\n"
        s += text + "\n"
    writeFile("extended-output1.txt", s)

def readOutputToMapping():
    s = readFile("extended-output2.txt")
    i = 0
    userIds = []
    genres = []
    tweets = []
    for l in s.split("\n"):
        if l == "":
            continue
        if i == 0:
            #print l
            userIds += [int(l)]
            i += 1
        elif i == 1:
            genres += [l]
            i += 1
        else:
            text = l
            tweets += [l]
            i = 0
    # genres and tweets are correct form input now to call to train_test

    ##############################
    # Our own bag of words code: #
    ##############################
    # genre_training = genres[0:390]
    # tweet_training = tweets[0:390]
    # genre_testing = genres[390:416]
    # tweet_testing = tweets[390:416]
    # (cond_freqs, genre_freqs, words_by_genre, genre_size) = tt.train_bow(genre_training, tweet_training)
    # tt.test_bow(cond_freqs, genre_freqs, words_by_genre, genre_size, tweet_testing, genre_testing)

    #########################
    # sklearn bag of words: #
    #########################
    # tt.train_test_sklearn(genres, tweets)



# writeToTextFile()
readOutputToMapping()