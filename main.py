import tweepy
import sys
import os
import logging
from threading import Thread
from sqlalchemy import Table
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base

import tweeting_script

'''
main file of bot. All other modules are called and implemented here
'''

def main():
'''
    #create twitter api
    my_api = create_api.create_api()

    #get database session
    my_session = db_connect.get_database()
'''

    DB_URL = os.environ['DATABASE_URL']
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    try:

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()
        print('Successfully created twitter API')

    except Exception as e:

        print('Error: Cannot create twitter api')
        raise e


    try:

        engine = create_engine(DB_URL, echo=True)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tweet_table = metadata.tables['tweets']
        session_maker = orm.sessionmaker(bind=engine, autoflush=True, autocommit-True, expire_on_commit=True)
        session = orm.scoped_session(session_maker)
        print('Successfully connected to database')

    except:

        sys.exit('Error: Cannot connect to database')



    #start tweeting script in a different thread
    tweeting_script_thread = Thread(target = tweeting_script.tweet_pipeline, args = (session, api))

    tweeting_script_thread.start()
    print('Started tweeting thread...')


if __name__ == "__main__":

    main()
