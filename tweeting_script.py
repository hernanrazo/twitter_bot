import tweepy
import os
import sys
import time
import random
import logging

import db_script
'''
contains all functions needed to post a tweet.
'''

<<<<<<< HEAD
logger = logging.getLogger()


def get_random_num():

    random_num = random.randrange(1, 52, 1)
    return random_num


def get_tweet(conn):

    try:

        num = get_random_num()
        tweet = db_script.read_query(conn, num)
        return tweet

    except:

        get_tweet(conn)
=======
    #WAIT_TIME_IN_SEC = 21600 #tweet roughly 4 times a day

logger = logging.getLogger()


def get_random_num():

    random_num = random.randrange(1, 52, 1)

    return random_num
>>>>>>> heroku/origin


def post_tweet(tweet, api):

    api.update_status(tweet)
    print('Successfully tweeted')
    sys.stdout.flush()

<<<<<<< HEAD

#combine all functions into one pipeline
def tweet_pipeline(conn, api):

    WAIT_TIME_IN_SEC = 21600
    empty_check = db_script.is_empty(conn)

    while(empty_check == 1):

        tweet = get_tweet(conn)
        post_tweet(tweet)
        db_script.delete_query(conn, tweet)
        conn.commit()
        time.sleep(WAIT_TIME_IN_SEC)

    else:

        print('Ran out of tweets')
        sys.stdout.flush()
        conn.close()
        return
=======
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






>>>>>>> heroku/origin
