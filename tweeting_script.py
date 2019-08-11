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

logger = logging.getLogger()

#return random munber between 1 and 52
def get_random_num():

    random_num = random.randrange(1, 52, 1)
    return random_num


#retrieve tweet from the database
def get_tweet(session):

    try:

        num = get_random_num()
        tweet = db_script.read_query(session, num)
        return tweet

    except:

        get_tweet(tweet)


#post to twitter
def post_tweet(tweet, api):

    api.update_status(tweet)
    print('Successfully tweeted')
    sys.stdout.flush()


#combine all functions into one pipeline
def tweet_pipeline(session, api):

    WAIT_TIME_IN_SEC = 21600
    empty_check = db_script.is_empty(session)

    while(empty_check == 1):

        tweet = get_tweet(session)
        post_tweet(tweet)
        db_script.delete_query(session, tweet)
        session.commit()
        time.sleep(WAIT_TIME_IN_SEC)

    else:

        print('Ran out of tweets')
        sys.stdout.flush()
        session.close()
        return
