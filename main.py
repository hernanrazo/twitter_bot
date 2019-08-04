import tweepy
import sys
import os
import logging
from threading import Thread

#custom imports
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
    my_api = create_api.create_api
    print('Created twitter API')
    sys.stdout.flush()

    #connect to database
    my_conn = db_connect.get_connection
    print('Created db connection')
    sys.stdout.flush()

    #start tweeting script in a different thread
    tweeting_script_thread = Thread(target = tweeting_script.tweet_pipeline, args = (my_conn, my_api))

    tweeting_script_thread.start()
    print('Started tweeting thread')
    sys.stdout.flush()



if __name__ == "__main__":

    main()
