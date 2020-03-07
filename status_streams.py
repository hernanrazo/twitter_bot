import tweepy
import os

import db_queries
import get_friends

#define class for the stream listener
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor
        #set counter to only get 1200 tweets
        self.counter = 0
        self.max = 1200

    #get tweets
    def on_status(self, status):
        if not status.retweeted:
            status_dict = {'created_at' : status.created_at.strftime('%y-%m-&d %H:%M'),
                           'source_stream' : 'general stream',
                           'status_id' : status.id_str,
                           'user_id' : status.user.id_str,
                           'screen_name' : status.user.name,
                           'tweet_text' : status.text,
                           'num_likes' : status.favorite_count,
                           'num_retweets' : status.retweet_count,
                           'favorited' : status.favorited}

            created_at = status_dict['created_at']
            source_stream = status_dict['source_stream']
            status_id = status_dict['status_id']
            user_id = status_dict['user_id']
            screen_name = status_dict['screen_name']
            tweet_text = status_dict['tweet_text']
            num_likes = status_dict['num_likes']
            num_retweets = status_dict['num_retweets']
            favorited = status_dict['favorited']

            db_queries.insert_raw_tweets_table(self.cursor, created_at, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets, favorited)

        self.counter +=1
        if self.counter == self.max:
            return False

    #ignore error where user cannot be found
    def on_error():
        if status_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass

#get tweets from list of friends
def friends_stream(api, cursor, user_name):
    try:
        for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended', include_rts=False, screen_name=user_name).items(1):
            #ignore retweets
            if not status.retweeted:
                status_dict = {'created_at' : status.created_at.strftime('%y-%m-%d %H:%M'),
                               'source_stream' : 'following stream',
                               'status_id' : status.id_str,
                               'user_id' : status.user.id_str,
                               'screen_name' : status.user.name,
                               'tweet_text' : status.full_text,
                               'num_likes' : status.favorite_count,
                               'num_retweets' : status.retweet_count,
                               'favorited' : status.favorited}

                created_at = status_dict['created_at']
                source_stream = status_dict['source_stream']
                status_id = status_dict['status_id']
                user_id = status_dict['user_id']
                screen_name = status_dict['screen_name']
                tweet_text = status_dict['tweet_text']
                num_likes = status_dict['num_likes']
                num_retweets = status_dict['num_retweets']
                favorited = status_dict['favorited']

                db_queries.insert_raw_tweets_table(cursor, created_at, source_stream, status_id, user_id, screen_name, tweet_text, num_likes, num_retweets, favorited)


    #ignore error where user cannot be found
    except tweepy.TweepError as e:
        if e.api_code == 179:
            print('Error trying to access tweets from user. Skipping to next user...')
            pass


#set streaming class and filter for the general stream
def general_stream(api, cursor):
    myStreamListener = MyStreamListener(cursor)
    stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    stream.filter(languages=['en'], track=['the'])


#set function that controls both streams
def streaming_pipeline(api, cursor):
    #get list of all users that are currently followed
    #iterate through the following_list and grab the single latest tweet
    print('getting following...')
    friends_list = get_friends.get_friends(api)
    for user in friends_list:
        f_stream = friends_stream(api, cursor, user)

    #start streams for tweets from general population
    general_stream(api, cursor)
