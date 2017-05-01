from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from nltk import ngrams

import numpy as np
import math

# takes in a list of genres (by individual), and a list of corresponding tweets for those individuals, and returns a 
# conditional frequency dictionary that contains P(word | genre) probabilities, as well as a dictionary of marginal 
# genre frequencies and a dictionary of total word counts by genre
def train_bow(genres, tweets, n_gram):

	Genres_set = set(genres)
	genre_freqs = {} # P(genre) dictionary
	conditional_freqs = {} # P(word | genre) dictionary
	words_by_genre = {} # number of words in each genre
	genre_size = len(genres)

	for g in Genres_set: # Establishing frequencies of each genre and creating a conditional frequencies dictionary
		genre_freqs[g] = (genres.count(g)/float(len(genres)))
		conditional_freqs[g] = {}

	for i in xrange(len(tweets)):
		gram_tweet = ngrams(tweets[i].split(), n_gram) # Splitting into a list of words
		new_tweet = []
		for item in gram_tweet:
			new_tweet.append(" ".join(item))
		if len(new_tweet) >= 10/n_gram:
			new_tweet = new_tweet[0:(10/n_gram)]
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

	return(conditional_freqs, genre_freqs, words_by_genre, genre_size)


# takes in a trained conditional frequency dicationary, a genre frequency dicationary, a word frequency by genre dictionary, 
# and a list of tweets and genres (test data), and returns the test predictoins for that testing set. 
def test_bow(conditional_freqs, genre_freqs, words_by_genre, genre_size, tweets, genres, n_gram):
	test_preds = []
	Genre_set = set(genre_freqs.keys())
	for tweet in tweets:
		gram_tweet = ngrams(tweet.split(), n_gram)
		new_tweet = []
		for item in gram_tweet:
			new_tweet.append(" ".join(item))
		logprobs_by_genre = {} # dictionary of the form genre : ~ P(genre | tweet)
		for genre in Genre_set:
			new_logprob = 0.0
			counter = 0
			while counter < 10:
				if new_tweet[counter] in conditional_freqs[genre].keys():
					new_logprob += math.log((conditional_freqs[genre][new_tweet[counter]]*words_by_genre[genre] + 1.0)/(words_by_genre[genre] + 10000)) # P(word1 | genre) * P(word2 | genre) * * * * P(wordn | genre)
																															 # but using smoothing
				else:
					new_logprob += math.log((0 + 1.0)/(words_by_genre[genre] + 10000)) # again, using smothing
				counter += 1
			new_logprob += math.log(genre_freqs[genre]) # . . . * P(genre)
			logprobs_by_genre[genre] = new_logprob

		# Finding the genre that maximizes the probability P(genre | tweet): 
		maxx = max(logprobs_by_genre.values()) 
		keys = [x for x,y in logprobs_by_genre.items() if y ==maxx] # here, we return all genres that maximize the probability above 
													  # (not just the first appearance)
		test_preds.append(keys)

	accuracy_count = 0
	for i in xrange(len(genres)):
		if genres[i] in test_preds[i]:
			accuracy_count += 1
	print("percent accuracy, :", accuracy_count/float(len(genres)))

	return(test_preds)




def train_test_sklearn(genres, tweets):
	nb = MultinomialNB()
	vect = CountVectorizer()
	vect.fit(tweets[0:390])
	simple_train_dtm = vect.transform(tweets[0:390])
	simple_train_dtm.toarray()
	simple_test_dtm = vect.transform(tweets[390:416])
	simple_test_dtm.toarray()
	nb.fit(simple_train_dtm, genres[0:390])
	pred_genres = nb.predict(simple_test_dtm)
	print(metrics.accuracy_score(genres[390:416], pred_genres))



