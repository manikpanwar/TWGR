import matplotlib.pyplot as plt

import getUserTweets as gut 
import csv
import train_test as tt
import re

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

# http://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
def removeUrls(t):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', t, flags=re.MULTILINE)

# http://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
def removeHashtags(t):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",t).split())

def getTweetsMap():
    d = readCsv()
    numUsers = 500
    numWordsPerUser = 200
    users = []
    for userId in d.keys()[:numUsers]:
        val = d[userId]
        # print userId, d[userId], 
        tweets = gut.getUserTweetsByUserID(userId)
        if tweets == "":
            continue
        
        tweets = ".".join(tweets.split("\n"))
        t = ' '.join(tweets.split(" ")[:numWordsPerUser])
        # d[userId] = (val, (t.encode('utf-8')).encode('ascii', errors='ignore'))
        t = removeUrls(t)
        t = removeHashtags(t)
        if t == "" or t == "\n": continue
        users += [userId]
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
    writeFile("extended-output5.txt", s)

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
    return(genres, tweets)



## Code for making figures: 

    # For comparing our model to sklearn: 
def compare_sklearn_graph(genres, tweets):

    ##############################
    # Our own bag of words code: #
    ##############################
    our_scatter = []
    sklearn_scatter = []
    chances = []
    for i in xrange(16, 396, 10):
        genre_training = genres[0:i]
        tweet_training = tweets[0:i]
        genre_testing = genres[i:i+20]
        tweet_testing = tweets[i:i+20]
        chance = 1/float(len(set(genres[0:i])))
        (cond_freqs, genre_freqs, words_by_genre, genre_size) = tt.train_bow(genre_training, tweet_training, 1)
        # print(i)
        our_accuracy = tt.test_bow(cond_freqs, genre_freqs, words_by_genre, genre_size, tweet_testing, genre_testing, 1)
    #########################
    # sklearn bag of words: #
    #########################
        sklearn_accuracy = tt.train_test_sklearn(genres, tweets, i)

        our_scatter.append(our_accuracy)
        sklearn_scatter.append(sklearn_accuracy)
        chances.append(chance)
    plt.figure()
    plt.title("Plot of Testing Accuracy Over Time,\nWith Prior Term for Our Model")
    plt.scatter(range(16, 396, 10), our_scatter, color="blue", label="our accuracy")
    plt.scatter(range(16, 396, 10), sklearn_scatter, color="red", label="sklearn accuracy")
    plt.scatter(range(16, 396, 10), chances, color="yellow", label="chance accuracy")
    plt.legend()
    plt.xlabel("Size of Entire Dataset (20 Testing and n-20 Training Instances)")
    plt.ylabel("Testing Accuracy (Percent out of 20 Testing Instances")
    plt.savefig("Testing_Acc_WithoutPrior.png")
    plt.show()




    # For displaying n-gram testing accuracy over time: 
def display_ngram(genres, tweets):

    ##############################
    # Our own bag of words code: #
    ##############################
    monogram = []
    bigram = []
    trigram = []
    chances = []
    for i in xrange(16, 396, 10):
        genre_training = genres[0:i]
        tweet_training = tweets[0:i]
        genre_testing = genres[i:i+20]
        tweet_testing = tweets[i:i+20]
        chance = 1/float(len(set(genres[0:i])))

        (mono_cond_freqs, mono_genre_freqs, mono_words_by_genre, mono_genre_size) = tt.train_bow(genre_training, tweet_training, 1)
        # print(i)
        mono = tt.test_bow(mono_cond_freqs, mono_genre_freqs, mono_words_by_genre, mono_genre_size, tweet_testing, genre_testing, 1)

        (bi_cond_freqs, bi_genre_freqs, bi_words_by_genre, bi_genre_size) = tt.train_bow(genre_training, tweet_training, 2)
        # print(i)
        bi = tt.test_bow(bi_cond_freqs, bi_genre_freqs, bi_words_by_genre, bi_genre_size, tweet_testing, genre_testing, 2)

        (tri_cond_freqs, tri_genre_freqs, tri_words_by_genre, tri_genre_size) = tt.train_bow(genre_training, tweet_training, 3)
        # print(i)
        tri = tt.test_bow(tri_cond_freqs, tri_genre_freqs, tri_words_by_genre, tri_genre_size, tweet_testing, genre_testing, 3)

        monogram.append(mono)
        bigram.append(bi)
        trigram.append(tri)
        chances.append(chance)

    plt.figure()
    plt.title("Plot of N-gram Testing Accuracy Over Time")
    plt.scatter(range(16, 396, 10), monogram, color="red", label="monogram accuracy")
    plt.scatter(range(16, 396, 10), bigram, color="blue", label="bigram accuracy")
    plt.scatter(range(16, 396, 10), trigram, color="green", label="trigram accuracy")
    plt.scatter(range(16, 396, 10), chances, color="yellow", label="chance accuracy")
    plt.legend()
    plt.xlabel("Size of Entire Dataset (20 Testing and n-20 Training Instances)")
    plt.ylabel("Testing Accuracy (Percent out of 20 Testing Instances")
    plt.savefig("N_gram.png")
    plt.show()



# writeToTextFile()
# readOutputToMapping()

# writeToTextFile()

# display_ngram(*readOutputToMapping())

# compare_sklearn_graph(*readOutputToMapping()) 
