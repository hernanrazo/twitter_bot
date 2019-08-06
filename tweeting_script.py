import tweepy
import os
import sys
import time
import random
import logging

'''
contains all functions needed to post a tweet.
'''

    #WAIT_TIME_IN_SEC = 21600 #tweet roughly 4 times a day

logger = logging.getLogger()


def get_random_num():

    random_num = random.randrange(1, 52, 1)

    return random_num


def post_tweet(tweet, api):

    api.update_status(tweet)
    logger.info('Successfully tweeted')


#combine all functions into one pipeline
def tweet_pipeline(conn, api):

    empty_check = db_script.is_empty(conn)

    if (empty_check == 1):

        num = get_random_num()
        tweet = db_script.read_query(conn, num)
        post_tweet(tweet)

    else:

        print('Ran out of tweets')
        sys.stdout.flush()
        return






