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
        #ignore retweets
        if not status.retweeted:

            status_dict = {'created_at': status.created_at.strftime('%y-%m-%d %H:%M'),
                           'source_stream': 'general stream',
                           'status_id': status.id_str,
                           'user_id': status.user.id_str,
                           'screen_name': status.user.name,
                           'tweet_text':status.text,
                           'num_likes':status.favorite_count,
                           'num_retweets':status.retweet_count}

            self.counter +=1
            if self.counter == self.max:
                cursor.close()
                return False
            else:
                return status_dict


    #ignore error where user cannot be found
    def on_error():
        if status_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass


#get tweets from list of followers
def following_stream(api, user_name):
    try:
        for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended', include_rts=False, screen_name=user_name).items(1):
            #ignore retweets
            if not status.retweeted:

                status_dict = {'created_at': status.created_at.strftime('%y-%m-%d %H:%M'),
                               'source_stream': 'following stream',
                               'status_id': status.id_str,
                               'user_id': status.user.id_str,
                               'screen_name': status.user.name,
                               'tweet_text':status.text,
                               'num_likes':status.favorite_count,
                               'num_retweets':status.retweet_count}
                return status_dict


    #ignore error where user cannot be found
    except tweepy.TweepError as e:
        if e.api_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass


#set streaming class and filter for the general stream
def general_stream(api):
    stream_listener = stream_listener_class()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(languages=['en'], track=['the'])


#set function that controls both streams
def streaming_pipeline(api, cursor):

    #get list of all users that are currently followed
    following_list = follow.get_following(api)

    #iterate through the following_list and grab the single latest tweet
    for user in following_list:
        f_stream = following_stream(api, user)

        created_at = f_stream['created_at']
        source_stream = f_stream['source_stream']
        status_id = f_stream['status_id']
        user_id = f_stream['user_id']
        screen_name = f_stream['screen_name']
        tweet_text = f_stream['tweet_text']
        num_likes = f_stream['num_likes']
        num_retweets = f_stream['num_retweets']

        db_queries_insert_raw_tweets_table(cursor, created_at, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets)

    #start streams for tweets from general population
    g_stream = general_stream(api)

    for item in g_stream:
        created_at = g_stream['created_at']
        source_stream = g_stream['source_stream']
        status_id = g_stream['status_id']
        user_id = g_stream['user_id']
        screen_name = g_stream['screen_name']
        tweet_text = g_stream['tweet_text']
        num_likes = g_stream['num_likes']
        num_retweets = g_stream['num_retweets']

        db_queries_insert_raw_tweets_table(cursor, created_at, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets)

    cursor.close()
