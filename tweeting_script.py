import tweepy
import os
import time
import logging
import natsort

'''
contains all functions needed to post a tweet.
'''


logger = logging.getLogger()

#get one giant list of all tweet file names
def get_file_names(file_path):

    file_names_array = []

    for infile in sorted(os.listdir(file_path)):
        if infile.endswith('.txt'):

            file_names_array.append(infile)

    natsort.natsorted(file_names_array, reverse = False)

    return file_names_array


#read the next tweet in line and post it
def read_tweet(name):

    f = open(name, "r")
    content = f.read()

    return content


def post_tweet(tweet, api):

    api.update_status(tweet)
    logger.info('Successfully tweeted')


#check if current tweet is below twitter's char limit
def char_limit_check(tweet):

    CHAR_LIMIT = 280

    if len(tweet) <= CHAR_LIMIT:
        return True
    else: 
        return False

#combine all functions into one pipeline
def tweet_pipeline(file_path, api):

    WAIT_TIME_IN_SEC = 21600 #tweet roughly 4 times a day
    counter = 0
    file_array = get_file_names(file_path)

    while counter != len(file_array):
        for i in file_array:

            tweet = read_tweet(file_path + i)

            if char_limit_check(tweet) == True:

                post_tweet(tweet, api)

            counter +=1
            time.sleep(WAIT_TIME_IN_SEC)
