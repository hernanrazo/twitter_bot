import tweepy
import os
import sys
import time
import random
import logging
import psycopg2

import db_script

'''
contains all functions needed to post a tweet.
'''
DB_URL = os.environ['DATABASE_URL']


#return random munber between 1 and 52
def get_random_num():

    random_num = random.randrange(1, 52, 1)
    print('Random number: %s' % (random_num))
    return random_num


#retrieve tweet from the database
def get_tweet(cursor):

    num = get_random_num()
    tweet = db_script.read_query(cursor, num)
    print(tweet)
    return tweet

#post to twitter
def post_tweet(tweet, api):

    api.update_status(tweet)
    print('Successfully tweeted')

#combine all functions into one pipeline
def tweet_pipeline(api):

    WAIT_TIME_IN_SEC = 21600
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        my_cursor = conn.cursor()
        print('Successfully connected to database')

    except:
        sys.exit('Error: Cannot connect to database')

    empty_check = db_script.is_empty(my_cursor)

    while empty_check==1:

        print('passed empty check')
        tweet = get_tweet(my_cursor)
        post_tweet(tweet, api)
        db_script.delete_query(my_cursor, tweet)
        conn.commit()

        print('Waiting for next tweet...')
        time.sleep(WAIT_TIME_IN_SEC)

    else:
        print('Ran out of tweets')
        my_cursor.close()
        conn.close()
        return
