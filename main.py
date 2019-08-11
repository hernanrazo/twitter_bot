import tweepy
import sys
import os
import logging
from threading import Thread
import create_api
import db_connect
import tweeting_script

'''
main file of bot. All other modules are called and implemented here
'''

def main():

    #get logger
    logger = logging.getLogger()

    #create twitter api
    my_api = create_api.create_api()
    print('Created twitter API')
    sys.stdout.flush()

    #get database session
    my_session = db_connect.get_database()
    print('Created db session')
    sys.stdout.flush()

    #start tweeting script in a different thread
    tweeting_script_thread = Thread(target = tweeting_script.tweet_pipeline, args = (my_session, my_api))

    tweeting_script_thread.start()
    print('Started tweeting thread')
    sys.stdout.flush()


if __name__ == "__main__":

    main()
