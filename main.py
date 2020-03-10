import tweepy
import sys
import os
import pandas as pd
from threading import Thread
import psycopg2
from psycopg2 import pool

import publish_status
import get_tweet_topic

'''main file of bot. All other modules are called and implemented here'''

def main():
    #credentials for twitter api and database in heroku
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

    DB_NAME = os.environ['DB_NAME']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']

    #retrieve saved pickles and model for topic extraction
    lda_model = pd.read_pickle('saved_pickles_models/lda_model.model')
    lda_id2word = pd.read_pickle('saved_pickles_models/train_id2word.pkl')
    lda_huber_classifier = pd.read_pickle('saved_pickles_models/huber_classifier.pkl')
    print('Successfully retrieved needed files for topic extraction...')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()
    print('Successfully created twitter API...')

    #create connection pool
    conn_pool = psycopg2.pool.ThreadedConnectionPool(2, 5, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME)

    if conn_pool:
        #get connection from pool, pass cursor as an argument, start tweeting script thread
        tweeting_conn = conn_pool.getconn()
        tweeting_thread = Thread(target=publish_status.tweet_pipeline, kwargs={'api':api, 'conn':tweeting_conn})
        tweeting_thread.start()
        print('Started tweeting thread...')
        tweeting_conn = conn_pool.getconn()
        #return connection when done
        conn_pool.putconn(tweeting_conn)
        print('Returned tweeting thread connection...')

        #get connection from pool, pass cursor as an argument, start topic extration thread
        topic_conn = conn_pool.getconn()
        topic_extraction_thread = Thread(target=get_tweet_topic.guess_topic_pipeline, kwargs={'api':api, 'conn': topic_conn, 'model': lda_model, 'corpus': lda_id2word, 'classifier': lda_huber_classifier})
        topic_extraction_thread.start()
        print('Started topic extraction thread...')
        #return connection when done
        conn_pool.putconn(topic_conn)
        print('Returned tweeting thread connection...')


if __name__ == "__main__":
    main()
