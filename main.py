import tweepy
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

    #get directory of all stored tweet filenames
    path = os.getcwd() + '/tweets/'

    #create the api
    my_api = create_api.create_api

    #connect to database
    my_conn = db_connect.get_connection

    #start tweeting script in a different thread
    tweeting_script_thread = Thread(target = tweeting_script.tweet_pipeline, args = (path, my_api))
    tweeting_script_thread.start()





if __name__ == "__main__":

    main()
