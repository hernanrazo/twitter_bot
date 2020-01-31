import tweepy
import sys
import os
from threading import Thread

import publish_status
import get_tweet_topic

'''
main file of bot. All other modules are called and implemented here
'''

def main():
    #credentials for twitter api in heroku
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    DB_URL = os.environ['DATABASE_URL']


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api.verify_credentials()
    print('Successfully created twitter API')
    

    conn = psycopg2.connect(DB_URL, sslmode='require')
    cursor = conn.cursor()
    print('Successfully connected to database')

    #retrieve saved pickles and model from training
    lda_model = pd.read_pickle('saved_pickles_models/lda_model.model')
    lda_id2word = pd.read_pickle('saved_pickles_models/train_id2word.pkl')
    lda_huber_classifier = pd.read_pickle('saved_pickles_models/huber_classifier.pkl')
    print('Successfully retrieved needed pickels for model...')

    #start tweeting script in a different thread
    tweeting_thread = Thread(target=publish_status.tweet_pipeline, kwargs={'api':api, 'cursor':cursor})
    tweeting_thread.start()
    print('Started tweeting thread...')

    #start tweet liking thread
    topic_thread = Thread(target=get_tweet_topic.guess_topic_pipline, kwargs={'api':api, 'cursor': cursor, 'model': lda_model, 'corpus': lda_id2word, 'classifier': lda_huber_classifier})
    topiv_thread.start()
    print('Started topic extraction thread...')

if __name__ == "__main__":

    main()
