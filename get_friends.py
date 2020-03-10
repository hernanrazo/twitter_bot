import tweepy
import time
import os

#compile list of currently followed users 
def get_friends(api):
    SCREEN_NAME = os.environ['SCREEN_NAME']
    friends_list = []
    friends = tweepy.Cursor(api.friends, screen_name=SCREEN_NAME).items()
    for user in friends:
        friends_list.append(user.screen_name)
    return friends_list
