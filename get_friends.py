import tweepy
import time


#compile list of currently followed users 
def get_friends(api):

    friends_list = []
    friends = tweepy.Cursor(api.friends, screen_name='WNUTSHANG').items()
    for user in friends:
        friends_list.append(user.screen_name)
    return following_list
