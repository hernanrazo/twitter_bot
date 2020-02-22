import tweepy
import os

import db_queries
import follow

#define class for the stream listener
class stream_listener_class(tweepy.StreamListener):

    def __init__(self):
        #set counter to only get 1200 tweets
        super().__init__()
        self.counter = 0
        self.max = 1200

    #get tweets
    def on_status(self, status):
            status = status.created_at.strftime('%y-%m-%d %H:%M')
            source_stream = 'general stream'
            status_id = status.id
            user_id = status.user_name.id_str
            screen_name =  user_name
            tweet_text = status.full_text
            num_likes = status.favorite_count
            num_retweets = status.retweet_count

            #insert everything into db
            insert_raw_tweets_table(cursor, status, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets)

            self.counter +=1
            if self.counter == self.max:
                return False


    #ignore error where user cannot be found
    def on_error():
        if status_code == 179:
            pass
        elif status_code == 420:
            return False


#get tweets from list of followers
def following_stream(api, cursor, user_name):
    try:
        for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended', include_rts=False, screen_name=user_name).items(1):

            status = status.created_at.strftime('%y-%m-%d %H:%M')
            source_stream = 'following stream'
            status_id = status.id_str
            user_id = status.user_name.id_str
            screen_name =  user_name
            tweet_text = status.full_text
            num_likes = status.favorite_count
            num_retweets = status.retweet_count

            insert_raw_tweets_table(cursor, status, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets)

    #ignore error where user cannot be found
    except tweepy.TweepError as e:
        if e.api_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass
        elif e.api_code == 420:
            return False


#set streaming class and filter for the general stream
def general_stream(api, cursor):
    stream_listener = stream_listener_class()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(languages=['en'], track=['the'])


#set function that controls both streams
def streaming_pipeline(api, cursor):
    #get list of all users that are currently followed
    following_list = follow.get_following(api)

    #iterate through the following_list and grab the single latest tweet
    for user in following_list:
        f_stream = following_stream(api, cursor, user)

    #start streams for tweets from general population
    g_stream = general_stream(api, cursor)
