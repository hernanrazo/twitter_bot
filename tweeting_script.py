import tweepy
import os
import time
import logging

'''
contains all functions needed to post a tweet.
'''

    #WAIT_TIME_IN_SEC = 21600 #tweet roughly 4 times a day

logger = logging.getLogger()

def post_tweet(tweet, api):

    api.update_status(tweet)
    logger.info('Successfully tweeted')


#combine all functions into one pipeline
def tweet_pipeline(conn, api):

    #do shit here

