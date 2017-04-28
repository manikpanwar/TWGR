# takes in a list of genres (by individual), and a list of corresponding tweets for those individuals, and returns a 
# conditional frequency dictionary that contains P(word | genre) probabilities, as well as a dictionary of marginal 
# genre frequencies and a dictionary of total word counts by genre
def train_bow(genres, tweets):

	Genres_set = set(genres)
	genre_freqs = {} # P(genre) dictionary
	conditional_freqs = {} # P(word | genre) dictionary
	words_by_genre = {} # number of words in each genre

	for g in Genres_set: # Establishing frequencies of each genre and creating a conditional frequencies dictionary
		genre_freqs[g] = (genres.count(g),len(genres))
		conditional_freqs[g] = {}

	for i in xrange(len(tweets)):
		new_tweet = tweets[i].split() # Splitting into a list of words
		if len(new_tweet) >= 100:
			new_tweet = new_tweet[0:100]
			new_genre = genres[i] # getting the genre that corresponds to this tweet
			if new_genre not in words_by_genre.keys(): 
				words_by_genre[new_genre] = 0.0
			for word in new_tweet: # "training" the conditional_freqs array
				if word in conditional_freqs[new_genre].keys(): 
					conditional_freqs[new_genre][word] += 1.0
				else:
					conditional_freqs[new_genre][word] = 1.0
				words_by_genre[new_genre] += 1

	for key in conditional_freqs.keys(): # iterating over genres
		for val in conditional_freqs[key].keys(): # iterating over words
			conditional_freqs[key][val] /= words_by_genre[key] # turning counts into frequencies

	return(conditional_freqs, genre_freqs, words_by_genre)


# takes in a trained conditional frequency dicationary, a genre frequency dicationary, a word frequency by genre dictionary, 
# and a list of tweets and genres (test data), and returns the test predictoins for that testing set. 
def test_bow(conditional_freqs, genre_freqs, words_by_genre, tweets, genres):
	Genres_set = set(genres)
	test_preds = []
	for tweet in tweets:
		new_tweet = tweet.split()
		probs_by_genre = {} # dictionary of the form genre : ~ P(genre | tweet)
		for genre in Genres_set:
			new_prob = 1.0
			for word in new_tweet:
				if conditional_freqs[genre][word] != 0:
					new_prob *= conditional_freqs[genre][word] # P(word1 | genre) * P(word2 | genre) * * * * P(wordn | genre)
				else:
					new_prob *= 1/float(words_by_genre[genre]) # sort of like "smoothing"
			new_prob *= genre_freqs[genre] # * P(genre)
			probs_by_genre[genre] = new_prob

		# Finding the genre that maximizes the probability P(genre | tweet): 
		maxx = max(probs_by_genre.values()) 
		keys = [x for x,y in dic.items() if y ==maxx] # here, we return all genres that maximize the probability above 
													  # (not just the first appearance)

	test_preds.append(keys)
	accuracy_count = 0
	for i in xrange(len(genres)):
		if genres[i] in test_preds[i]:
			accuracy_count += 1
	print("percent accuracy, :", accuracy_count/float(len(genres)))

	return(test_preds)

