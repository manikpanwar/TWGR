import re


def removeMentions(tweet):
    # return tweet
    return re.sub('@*\\s*', '', tweet)


# http://stackoverflow.com/questions/21589254/remove-urls-from-strings
def removeHyperLinks(tweet):
    return re.sub('http\\S+\\s*', '', tweet)

def processTweet(tweet):
    tweet = removeHyperLinks(tweet) # removes https://* links from a tweet
    # tweet = removeMentions(tweet)   # removes @user-name phrases from a tweet
    return tweet