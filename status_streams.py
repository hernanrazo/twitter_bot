import tweepy
import os

import db_queries
import follow

#define class for the stream listener
class StreamListener(self, StreamListener):

    def __init__(self):
        super().__inti__()
        self.counter = 0
        sefl.max = 1200

    #get tweets
    def on_status(self, status):
        obj = {'createdAt': status.created_at.strftime('%Y-%m-%d %H:%M'),
               'sourceStream': 'general stream',
               'statusID': status.id_str,
               'userID': status.id_str,
               'screenName': status.user.screen_name,
               'tweetText': status.text,
               'numLikes': status.favorite_count,
               'numRetweets': status.retweet_count}

        self.counter +=1
        if self.counter == self.max:
            return False
        else:
            return obj


    #ignore error where user cannot be found
    def on_error():
        if status_code ==179:
            pass


#get tweets from list of followers
def following_stream(api, user_name):
    try:
        for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended', include_rts=False, screen_name=user_name).items(1):
            return {'createdAt': status.created_at.strftime('%y-%m-%d %H:%M'),
                    'sourceStream': 'following stream',
                    'statusID': status.id_str,
                    'userID': status.user_name.id_str,
                    'screenName': user_name,
                    'tweetText': status.full_text,
                    'numLikes': status.favorite_count,
                    'numRetweets': status.retweet_count}

    #ignore error where user cannot be found
    except tweepy.TweepError as e:
        if e.api_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass


#set streaming class and filter for the general stream
def general_stream(api):
    StreamListener = StreamListener()
    stream = tweepy.Stream(api, StreamListener)
    stream.filter(languages=['en'], track=['the'])


#set function that controls both streams
def streaming_pipeline(api):
    #get list of all users that are currently followed
    following_list = follow.get_following(api)

    #iterate through the following_list and grab the single latest tweet
    for user in following_list:
        f_stream = following_stream(api, user)

        #insert info into db
        db_queries.insert_raw_tweets_table(f_stream['createdAt'],
                                           f_stream['sourceStream',
                                           f_stream['statusID'],
                                           f_stream['userID'],
                                           f_stream['screenName'],
                                           f_stream['tweetText'],
                                           f_stream['numLikes']
                                           f_stream['numRetweets'])


    #start stream for tweets from general population
    g_stream = general_stream(api)

    #insert infointo db
    db_queries.insert_raw_tweets_table(g_stream['createdAt'],
                                       g_stream['sourceStream'],
                                       g_stream['statusID'],
                                       g_stream['userID'],
                                       g_stream['screenName'],
                                       g_stream['tweetText'],
                                       g_stream['numLikes'],
                                       g_stream['numRetweets'])
