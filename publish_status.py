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

#retrieve tweet from the database
def get_tweet(cursor, selected_id):

    tweet = db_script.read_query(cursor, selected_id)
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
        DB_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DB_URL, sslmode='require')
        my_cursor = conn.cursor()
        print('Successfully connected to database')

    except:
        sys.exit('Error: Cannot connect to database')

    empty_check = db_script.is_empty(my_cursor)

    while empty_check==1:

        print('Passed empty check')
        tweet_id = db_script.get_id(my_cursor)
        tweet = get_tweet(my_cursor, tweet_id)
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
