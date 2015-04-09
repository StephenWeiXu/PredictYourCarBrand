
''' Data Preprocessing Functions
Please write your data preocessing method here, including PCA, SMOTE, CMU Research etc
rhz: filter (extract frequent words)
'''

import sys
import numpy as np
import os
from preprocess import preprocess
import operator
import re

''' Print the statistics of the car brand label '''
def printStats(label):
	car_brands = {0:'bmw', 1:'honda', 2:'jeep', 3:'audi', 4:'ford', 5:'hyundai', 6:'kia', 7:'lexus', 8:'mazda', 9:'nissan', 10:'toyota', 11:'ferrari'}

	label = list(label)
	label_unique = list(set(label))
	for item in label_unique:
		print item, car_brands[item],label.count(item)


# filter out all infrequent words (rhz)
def filter():
    N = 200
    tweet_collect = {} 				# tweet collection categorized by brands, key: brand, value: dicts of tweets
    for file in os.listdir('Complte Dataset'):
    	if 'DS' in file:
            continue

        # extract user_id and car brand from the filename
        data_file_name_split = re.split('\.', file)
        user_id = data_file_name_split[0]
        brand = data_file_name_split[1]

        # read the whole data and preprocess
        with open('Complte Dataset/'+file, 'r') as f:
        	str = f.readline()
        user_dict = preprocess(str)              # dict of this user, key: words, value: # of occurences

        brand_dict = tweet_collect.get(brand, None)    # dict of all the tweets by all the users the this brand 
        if brand_dict is None:
        	brand_dict = {}
        	tweet_collect[brand] = brand_dict

        brand_dict[user_id] = user_dict

    # stats of words occurences for each of the brand, pick up the N most
    # frequent for each brand and merge them into one vocabulary
    old = 0
    voc = set([])
    for brand in tweet_collect.keys():
        word_occu = {}
        brand_dict = tweet_collect[brand]
        for user_id in brand_dict:
            user_dict = brand_dict[user_id]
            for word in user_dict.keys():
                word_occu[word] = word_occu.get(word, 0) + user_dict[word]
                old += user_dict[word]

        # sort word_occu by value (occurence)
        sorted_list = sorted(word_occu.items(), key=operator.itemgetter(1), reverse = True)
        for i in range(N):
            voc.add(sorted_list[i][0])

    new = 0
    # reconstruct the collection by the filtered vocabulary
    for brand in tweet_collect.keys():
        brand_dict = tweet_collect[brand]
        for user_id in brand_dict.keys():
            old_user_dict = brand_dict[user_id]
            brand_dict[user_id] = {}
            new_user_dict = brand_dict[user_id]
            for word in voc:
                new_user_dict[word] = old_user_dict.get(word, 0)
                new += new_user_dict[word]

    print old, new
    return tweet_collect

filter()









