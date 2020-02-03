import tweepy
import time


#compile list of currently followed users 
def get_following(api):

    following_list = []
    following = tweepy.Cursor(api.followers, screen_name='WNUTSHANG').items()
    for user in following:
        followers_list.append(user.screen_name)

    return followers_list

'''
def follow_back(followers):
    
    for follower in followers:
        if not follwer.following:
            #retrieve first n tweets here
            #check if tweets are revelent
            #if relevent, follow back
            #if not, ignore
            #do this once a week???
'''
