import tweepy
import os
import sys
import time
import random

import db_queries

'''
contains all functions needed to post a tweet.
'''

#retrieve tweet from the database
def get_status(cursor, selected_id):
    tweet = db_script.read_query(cursor, selected_id)
    print(tweet)
    return tweet


#post to twitter
def post_status(status, api):
    api.update_status(status)
    print('Successfully tweeted')


#combine all functions into one pipeline
def tweet_pipeline(api, conn):
    WAIT_TIME_IN_SEC = 21600
    cursor = conn.cursor()
    empty_check = db_queries.empty_check_tweets(cursor)

    while empty_check==1:
        print('Passed empty check')
        status_id = db_script.read_id(cursor)
        status= get_status(cursor, status_id)
        post_status(status, api)
        db_script.delete_query(cursor, status)
        conn.commit()
        print('Waiting for next tweet...')
        time.sleep(WAIT_TIME_IN_SEC)

    else:
        print('Ran out of tweets')
        cursor.close()
        pass
