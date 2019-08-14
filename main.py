import tweepy
import sys
import os
import logging
import psycopg2
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

import tweeting_script

'''
main file of bot. All other modules are called and implemented here
'''

def main():

    #set all api credentials and database credentials
    DB_URL = os.environ['DATABASE_URL']
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    #log into twitter api
    try:

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()
        print('Successfully created twitter API')

    except Exception as e:

        print('Error: Cannot create twitter api')
        raise e


    #log into database
    try:

        conn = psycopg2.connect(DB_URL, sslmode='require')

        #engine = create_engine(DB_URL, echo=False)
        #metadata = MetaData(bind=None)
        #tweets_table = Table('tweets', metadata, autoload=True, autoload_with=engine)
        print('Successfully retrieved table')

    except:

        #quit program if database cannot be reached
        sys.exit('Error: Cannot communicate with database')


    #start tweeting script in a different thread
#    tweeting_script_thread = Thread(target = tweeting_script.tweet_pipeline, args = (tweets_table, api))

 #   tweeting_script_thread.start()
    print('Started tweeting thread...')

if __name__ == "__main__":

    main()
