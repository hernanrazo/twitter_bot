import tweepy
import os

import follow

class StreamListener(self, StreamListener):

    def on_status(self, status):
        #call model here
        print(status.text)

    def on_error(self, status_code):
        if status_code == 179:
            pass


#get tweets from list of followers
def get_tweets_from_following(api, following_list):

    try:
        for follower in following_list:
            following_tweets = api.user_timeline(screen_name=follower, tweet_mode='extended', count=1)
            return following_tweets

    except tweepy.TweepError as e:

        if e.api_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass


def get_tweet_stream(api):

    StreamListener = StreamListener()
    stream = tweepy.Stream(api, StreamListener)
    stream.filter(languages=['en'], track=['the'])


'''
def streams_pipeline(api):

    following_list = follow.get_following()
'''
