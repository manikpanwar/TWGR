import twitter

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

def getapi():
    credentialsFile = "twitter_access_keys.txt"
    text = readFile(credentialsFile).split("\n")
    consumer_key = text[0]
    consumer_secret = text[1]
    access_token_key = text[2]
    access_token_secret = text[3]


    api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)
    return api


def getUserTweetsByUserName():
    api = getapi()

    # print api.VerifyCredentials()

    user = 'blah'

    while user != "":
        user = raw_input("")
        statuses = api.GetUserTimeline(screen_name=user)
        for s in statuses:
            print s.text

def getUserTweetsByUserID():
    api = getapi()

    # print api.VerifyCredentials()

    userid = 'blah'

    while userid != "":
        userid = raw_input("")
        user = api.GetUser(userid)
        print user
        username = user.screen_name
        statuses = api.GetUserTimeline(screen_name=user)
        for s in statuses:
            print s.text


getUserTweetsByUserID()