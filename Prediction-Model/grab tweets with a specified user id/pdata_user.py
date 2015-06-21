'''
This can be used to crawl tweets of a specified user id. We will crawl the lastest 200 tweets of an user, if the user has not posted 200 tweets, we just crawl as much as they posted. We will remove texts which contains '@' and 'http'. To run this file, a csv file named user_id.csv must be exists in the same directory with this file, which includes user id and corresponding car label. The output is a directory named Complete Datasets, which contains a set of csv file, named by <useid>.<car_branch>.csv, which contains crawled tweets of that user.
'''
import twitter
import csv
import re
import time
import os

def textProcessing(tweetText, user_label): #text processing to remove texts that contain '@' and 'http'
    tweetText_list = tweetText.lower().split()
    for ind in range(0, len(tweetText_list)):
        for word in tweetText_list:
            if '@' in word or 'http' in word:
                tweetText_list.remove(word)
            elif user_label in word:
                tweetText_list.remove(word)
    tweetText_string = ' '.join(tweetText_list)
    return tweetText_string


api = twitter.Api(consumer_key = 'wfU6nyT3GroxdPX2F7jerlhGG',
consumer_secret = '0v7H1pWfEpsSChCd5ZsRAkL7hGNcxmBby1DUtYq0ehaGyOfnXR',
access_token_key = '2586502365-3u24Ea0wYAZc6np2lUY7FoOOZoVhTQspL7H3xuw',
access_token_secret = 'nZAM8wwwXiJM0Fq9Yj0DuEqULJS0GSvVgRXmRuwX87wq4')

userID_file = open('user_id.csv', 'r') #user_id.csv is a file storing user id and car label
line = userID_file.readline()

while 1:
    if len(line) == 0:
        break
    try:
        content = re.split(',', line)
        userid = content[0]
        user_label = content[1][0:(len(content[1])-2)] #corresponding car branch
        print userid
        
        dir_name = 'Complete Datasets/'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        file_name = dir_name + str(userid) + '.' + user_label + '.csv'
        twitter_f = open(file_name, 'w')
        twitter_c = csv.writer(twitter_f)
        statuses = api.GetUserTimeline(user_id = userid, count = 200) #twitter API to get 200 the most recent tweets with specified user id
        count = 0
        for s in statuses: # processing each tweet
            ss = str(s.text.encode('utf-8')).rstrip() #decode tweets
            ss_tp = textProcessing(ss, user_label)
            twitter_c.writerow([ss_tp])
        line = userID_file.readline()
        time.sleep(7) #there is a rate limit in twitter API, so we set a sleep manually to aviod exceed rate limit
        twitter_f.close()
    except BaseException, e: # output errors
        print 'failed on data ', str(e)
        line = userID_file.readline()
        time.sleep(7)
userID_file.close()
