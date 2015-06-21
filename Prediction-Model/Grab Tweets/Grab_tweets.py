
'''Description: 
This program uses Tweepy package to access Twitter API for grabing the tweets data from Twitter.
Line 46 will specify the maximum number of tweets you want to retrieve
The grabed tweets are output into a csv file called "Grab_tweets.csv" 

Please make sure that you have installed Tweepy package as describled in README file before running this code
'''

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
import time
import re

consumer_key = 'of1Ta5D471yKSSrfKeKrAwfBo'
consumer_secret = 'DB8bCGltzWiFm5gbfARhtRB3XScwxX5GWf6VZaYbPUI1nFUXf9'
access_token = '1356806936-q83gBJ56JbdrjWBp39dmmHcusiNQRxCWvjvmtVH'
access_token_secret = 'GgvR7jsXKeFEHaj9B1sUnzpuApQ5enDd9kH849lKl0ISU'
consumer_key = 'YdwqgugZRKoTxSSjeHoxmVmEk'
consumer_secret = 'EOfJpkD4oJvhTTxsTOTBCQASjvoW898DoldjiV1lnr8q6G9Vly'
access_token = '239362428-TeLTQymnVDuj2INy5Ocq5tba3CGBqoEG2lVBtPRs'
access_token_secret = 'YsyXPgsCjIBmx5c3FtCT4kKqB61xPuaaNcoG1Efg7Zf8N'

# Tweepy class for grabing tweets data
class listener(StreamListener):

    num_tweets = 0

    def on_data(self, data):
    	try:
    		#tweet = data.split(',"text":"')[1].split('","source":"')[0]
            raw_tweet = json.loads(data)
            spec_tweet = {}

            if raw_tweet.get('text', None) is None or raw_tweet.get('user', None) is None or str(raw_tweet.get('lang')) != 'en':
                return True
            raw_tweet['text'] = textProcessing(raw_tweet['text'])
            car_label = get_label(raw_tweet['text'], car_brand_list)

            if car_label != '':
                listener.num_tweets += 1
                print "%d tweets retrieved!" %(listener.num_tweets)
                if listener.num_tweets > 5000: # Set the number of tweets to be retrieved
                    print "\nTotal Number of tweets retrieved: ", listener.num_tweets-1
                    return False
                for attribute in attributes:
                    if 'user_id' == attribute:
                        if raw_tweet.get('user', None) is not None:
                            user_id = raw_tweet['user']['id_str']
                            spec_tweet['user_id'] = str(user_id.encode('utf-8')).rstrip()
                    else:
                        if raw_tweet.get(attribute, None) is not None:
                            spec_tweet[attribute] = str(raw_tweet[attribute].encode('utf-8')).rstrip()
                spec_tweet['brand'] = car_label
                with open ('Grab_tweets.csv', 'a') as f_tweet:
                    writer = csv.DictWriter(f_tweet, fieldnames = attributes, delimiter = '|')
                    writer.writerow(spec_tweet)

        	return True
        except BaseException, e:
        	print 'failed on_data, ', str(e)
        	time.sleep(1)

    def on_error(self, status):
       print status

''' 
Description: Process the tweet text, avoid irrelevant words being misassigned as car brand
Output: Processed tweet
'''
def textProcessing(tweetText):
    if re.match('rt\s', tweetText.lower()):
        print 'this is a retweet'
        print tweetText
        return ''

    tweetText_list = tweetText.lower().split()
    for ind in range(0, len(tweetText_list)):
        for word in tweetText_list:
            if '@' in word or 'http' in word:
                tweetText_list.remove(word)
    tweetText_string = ' '.join(tweetText_list)

    return tweetText_string

''' 
Description: Get car brands from local file
Output: a list of car brands for which we want to grab the relevant tweets
'''
def carBrandList():
    f_carBrand = open('car_brand.txt')
    car_brand = f_carBrand.read().lower().splitlines()
    car_brand = [token for token in car_brand if '#' not in token and len(token) != 0]
    f_carBrand.close()
    return car_brand

'''
Description: Compare and see if the grabed tweet does match certain car brand. If yes, return the car brand, else return ''
Output: the assigned car label for this tweet
'''
def get_label(tweetText, carBrandList):
    label = ''
    tweetText_list = tweetText.lower().split()
    for brand in carBrandList:
        if brand.lower() in tweetText_list:
            return brand
    return label

'''main program '''
car_brand_list = carBrandList()
filter_list = carBrandList()
for ind in range(0, len(car_brand_list)):
    filter_list[ind] = "my " + filter_list[ind]
attributes = ['user_id', 'brand', 'text']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=filter_list)


