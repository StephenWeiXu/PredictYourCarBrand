
# Using Twitter API for grabing the tweets data from Twitter 

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

consumer_key = 'gvUJ9I8YiQHaw2M0Fcfou2CC3'
consumer_secret = 'hvzuD9QjrhnuEhZvvw79jvHfApgtW2DfzlPFQauR26TQEE9TxB'
access_token = '1356806936-M0YK8ZD2ctd7qPOeaVlwBlJwHgqAjzBBig2DeNS'
access_token_secret = 'T7hFnK0HGLuPLIC8Enxn4ecv2Ogf0cxDl4mqQ1BsDVSW3'

class listener(StreamListener):

    def on_data(self, data):
    	try:
    		tweet = data.split(',"text":"')[1].split('","source":"')[0]

    		saveThis = str(time.time()) + '::' + tweet
	        saveFile = open('tweet_processed.txt', 'a')
	        saveFile.write(saveThis)
	        saveFile.write('\n')
	        saveFile.close()
        	return True
        except BaseException, e:
        	print 'failed on_data, ', str(e)
        	time.sleep(5)

    def on_error(self, status):
        print status

def carBrandList(:)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])
