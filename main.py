import tweepy
import sys
import os
from threading import Thread

import publish_status
import db_script
import get_tweet_topic

'''
main file of bot. All other modules are called and implemented here
'''

def main():
    #credectials for twitter api in heroku
    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']


    #create twitter api
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()
        print('Successfully created twitter API')

    except Exception as e:
        print('Error creating twitter API')
        raise e


    #connect to database
    try:
        DB_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DB_URL, sslmode='require')
        cursor = conn.cursor()
        print('Successfully connected to database')

    except:
        sys.exit('Error: Cannot connect to database')

    #retrieve saved pickles and model from training
    lda_model = pd.read_pickle('saved_pickles_models/lda_model.model')
    lda_id2word = pd.read_pickle('saved_pickles_models/train_id2word.pkl')
    lda_huber_classifier = pd.read_pickle('saved_pickles_models/huber_classifier.pkl')


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
