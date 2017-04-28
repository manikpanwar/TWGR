import csv
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

users = {} # This will become the dictionary of user:move_genres

all_genres = set([]) # This will become a set of all movie genres mentioned in the dataset

movie_genres = {} # This will be a dictionary of movie:genres; i.e. a dictionary of all of the 
# genre's that each movie belongs to

get_twitter = {} # This will be a dictionary of user_id:twitter_id pairs

with open('movies.dat', 'r') as movies: # Setting up the movie_genres and all_genres dictionaries
	for row in movies.readlines():
		new_row = row.split("::")
		new_row += new_row[-1].split("|") 
		new_row.pop(1)
		new_row.pop(1)
		new_row[-1] = new_row[-1].strip("\n")
		movie_genres[new_row[0]] = new_row[1:]
		all_genres = all_genres.union(set(new_row[1:]))

def generate_user_dict(): # This will create a personal dictionary 
# for each user in the users dicionary
	result = {}
	for G in all_genres:
		result[G] = []
	return result

with open('ratings.dat', 'r') as ratings: # Setting up the users dictionary
	for row in ratings.readlines():
		new_row = row.split("::")
		new_row.pop(-1)
		if new_row[0] in users.keys():
			for g in movie_genres[new_row[1]]:
				users[new_row[0]][g].append(int(new_row[2]))
		else:
			users[new_row[0]] = generate_user_dict()
			for g in movie_genres[new_row[1]]:
				users[new_row[0]][g].append(int(new_row[2]))

with open ('users.dat', 'r') as IDS: # Setting up the user_id:twitter_id pairings
	for row in IDS.readlines():
		new_row = row.split("::")
		get_twitter[new_row[0]] = new_row[1]




cleaned_dict = {}

for user_id in users.keys(): # Finding the "favorite" movie genre for each person
	max_key = ""
	most_key = ""
	max_mean = 0
	max_ratings = 0
	for g in users[user_id].keys():
		if len(users[user_id][g]) > 0:
			new_mean = np.mean(users[user_id][g])
			if new_mean >= max_mean:
				max_mean = new_mean
				max_key = g
	cleaned_dict[get_twitter[user_id]] = max_key

w = csv.writer(open("output.csv", "w"))
for key, val in cleaned_dict.items():
    w.writerow([key, val])