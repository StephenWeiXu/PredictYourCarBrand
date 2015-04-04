
# Using Twitter API for grabing the tweets data from Twitter

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
import time
import re

<<<<<<< HEAD
consumer_key = 'of1Ta5D471yKSSrfKeKrAwfBo'
consumer_secret = 'DB8bCGltzWiFm5gbfARhtRB3XScwxX5GWf6VZaYbPUI1nFUXf9'
access_token = '1356806936-q83gBJ56JbdrjWBp39dmmHcusiNQRxCWvjvmtVH'
access_token_secret = 'GgvR7jsXKeFEHaj9B1sUnzpuApQ5enDd9kH849lKl0ISU'
=======
consumer_key = 'YdwqgugZRKoTxSSjeHoxmVmEk'
consumer_secret = 'EOfJpkD4oJvhTTxsTOTBCQASjvoW898DoldjiV1lnr8q6G9Vly'
access_token = '239362428-TeLTQymnVDuj2INy5Ocq5tba3CGBqoEG2lVBtPRs'
access_token_secret = 'YsyXPgsCjIBmx5c3FtCT4kKqB61xPuaaNcoG1Efg7Zf8N'
>>>>>>> 8e400f51f108b56f6ab0ef63117d35ca142e467c

class listener(StreamListener):

    num_tweets = 0

    def on_data(self, data):
<<<<<<< HEAD
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
                            if user_id in existing_id:
                                #print 'User ID already existent'
                                return True
                            spec_tweet['user_id'] = str(user_id.encode('utf-8')).rstrip()
                    else:
                        if raw_tweet.get(attribute, None) is not None:
                            spec_tweet[attribute] = str(raw_tweet[attribute].encode('utf-8')).rstrip()
                spec_tweet['brand'] = car_label
                with open ('additional_tweet_wei.csv', 'a') as f_tweet:
                    writer = csv.DictWriter(f_tweet, fieldnames = attributes, delimiter = '|')
                    writer.writerow(spec_tweet)

        	return True
        except BaseException, e:
        	print 'failed on_data, ', str(e)
        	time.sleep(1)
=======

        #tweet = data.split(',"text":"')[1].split('","source":"')[0]
        raw_tweet = json.loads(data)
        spec_tweet = {}
        if raw_tweet.get('text', None) is None or raw_tweet.get('user', None) is None or str(raw_tweet.get('lang')) != 'en':
            return True
        raw_tweet['text'] = textProcessing(raw_tweet['text'])
        car_label = get_label(raw_tweet['text'], car_brand_list)
        if car_label == '':
            return True
        spec_tweet['brand'] = car_label
        spec_tweet['text'] = str(raw_tweet['text'].encode('utf-8')).rstrip()
        user_id = raw_tweet['user']['id_str']
        spec_tweet['user_id'] = str(user_id.encode('utf-8')).rstrip()

        if spec_tweet['user_id'] + spec_tweet['text'] in exist_addition:
            print 'Tweet text + userid already in additional_tweet.csv'
            return True
        exist_addition.append(spec_tweet['user_id'] + spec_tweet['text'])
        if spec_tweet['user_id'] in existing_id:
            print 'User ID already existent'
            return True

        listener.num_tweets += 1
        print "%d tweets retrieved!" %(listener.num_tweets)
        '''
        if listener.num_tweets > 5000: # Set the number of tweets to be retrieved
            print "\nTotal Number of tweets retrieved: ", listener.num_tweets-1
            return False
        '''

        with open ('additional_tweet.csv', 'a') as f_tweet:
            writer = csv.DictWriter(f_tweet, fieldnames = attributes, delimiter = '|')
            print spec_tweet
            writer.writerow(spec_tweet)
        return True
>>>>>>> 8e400f51f108b56f6ab0ef63117d35ca142e467c

    def on_error(self, status):
       print status

# Process the tweet text, avoid irrelevant words being misassigned as car brand
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

def carBrandList():
    f_carBrand = open('car_brand.txt')
    car_brand = f_carBrand.read().lower().splitlines()
    car_brand = [token for token in car_brand if '#' not in token and len(token) != 0]
    f_carBrand.close()
    return car_brand

def get_label(tweetText, carBrandList):
    '''
    infer car brand from the tweet text
    '''
    label = ''
    tweetText_list = tweetText.lower().split()
    for brand in carBrandList:
        if brand.lower() in tweetText_list:
            return brand
    return label

# loading the existing user id
existing_id = []
with open('tweet_data_all_5000.csv', 'r') as f:
    id_reader = csv.reader(f, delimiter='|')
    for row in id_reader:
        existing_id.append(row[0])

exist_addition = []
with open('additional_tweet.csv', 'r') as f:
    id_reader = csv.reader(f, delimiter='|')
    for row in id_reader:
        existing_id.append(row[0] + row[1])

car_brand_list = carBrandList()
filter_list = carBrandList()
for ind in range(0, len(car_brand_list)):
    filter_list[ind] = "my " + filter_list[ind]
attributes = ['user_id', 'brand', 'text']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=filter_list)


