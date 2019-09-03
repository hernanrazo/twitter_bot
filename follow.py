import tweepy
import time

'''
steps:
    get list of all followers
    if not already following, follow them back

code that follows people.
follow new followers
follow people that favored a tweet
follow people that commented on a post
follow people that retweeted a post
'''

#compile list of followers
def get_followers(api):

    followers_list = []
    followers = tweepy.Cursor(api.followers, screen_name='WNUTSHANG').items()
    for user in followers:
        followers_list.append(user.screen_name)

    return followers_list

#get tweets from list of followers
def get_tweets_from_followers(api, followers):

    for follower in followers:
        follower_tweets = api.timeline(screen_name=follower, tweet_mode='extended', count=10)
        return follower_tweets


def follow_back(followers):
    
    for follower in followers:
        if not follwer.following:
            #retrieve first n tweets here
            #check if tweets are revelent
            #if relevent, follow back
            #if not, ignore
            #do this once a week???
