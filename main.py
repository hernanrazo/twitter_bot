import tweepy
import sys
import os
import logging
from threading import Thread

import create_api
import publish_status

'''
main file of bot. All other modules are called and implemented here
'''

def main():

    #create twitter api
    twitter_api = create_api.create_api()

    #start tweeting script in a different thread
    tweeting_thread = Thread(target = publish_status.tweet_pipeline, kwargs={'api':twitter_api})

    tweeting_thread.start()
    print('Started tweeting thread...')

if __name__ == "__main__":

    main()
