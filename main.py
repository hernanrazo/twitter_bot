import tweepy
import sys
import os
import pandas as pd
from threading import Thread
import psycopg2
from psycopg2 import ThreadedConnectionPool

import publish_status
import get_tweet_topic

'''
main file of bot. All other modules are called and implemented here
'''

def main():
    #credentials for twitter api and database in heroku
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    DB_URL = os.environ['DATABASE_URL']
    DB_NAME = os.environ['DB_NAME']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']


    #retrieve saved pickles and model for topic extraction
    lda_model = pd.read_pickle('saved_pickles_models/lda_model.model')
    lda_id2word = pd.read_pickle('saved_pickles_models/train_id2word.pkl')
    lda_huber_classifier = pd.read_pickle('saved_pickles_models/huber_classifier.pkl')
    print('Successfully retrieved needed pickles for topic extraction...')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()
    print('Successfully created twitter API')

    #pass a conn to each thread
    #go to each thread pipeline and configure a cursor and its proper closing feature
    #close the pool in main.py






    #create connection pool
    conn_pool = psycopg2.pool.ThreadedConnectionPool(2, 5, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME)

    if conn_pool:
        #get connection from pool, pass cursor as an argument, start tweeting script thread
        #return connection when done
        tweeting_conn = conn_pool.get_conn()
        tweeting_cursor = tweeting_conn.cursor()
        tweeting_thread = Thread(target=publish_status.tweet_pipeline, kwargs={'api':api, 'tweeting_cursor':cursor})
        tweeting_thread.start()
        print('Started tweeting thread...')
        conn_pool.putconn(tweeting_conn)
        print('returned tweeting thread connection...')


        #get connection from pool, pass cursor as an argument,start tweet liking thread
        #return connection when done
        topic_conn = conn_pool.get_conn()
        topic_cursor = topic_conn.cursor()
        topic_thread = Thread(target=get_tweet_topic.guess_topic_pipeline, kwargs={'api':api, 'cursor': cursor, 'model': lda_model, 'corpus': lda_id2word, 'classifier': lda_huber_classifier})
        topic_thread.start()
        print('Started topic extraction thread...')
        conn_pool.putconn(topic_conn)
        print('returned tweeting thread connection...')


if __name__ == "__main__":

    main()
