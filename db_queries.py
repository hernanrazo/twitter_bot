import psycopg2
import random

'''
all functions relating to direct db interaction
'''

#check if table is empty. return 1 if yes, 0 if not
def is_empty(cursor):
    cursor.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = cursor.fetchone()
    return int(result[0])


'''
===============================================================================
========================retrieving info stuff==================================
===============================================================================
'''
#grab a random tweet
def read_id(cursor):
    select_query = cursor.execute('SELECT id FROM tweets')
    result = cursor.fetchall()
    selected_id = random.choice(result)
    print(selected_id)
    return selected_id


#get tweet that matches the given id
def read_query(cursor, tweet_id):
    cursor.execute('SELECT tweet FROM tweets WHERE id = %s', (tweet_id,))
    result = cursor.fetchone()
    return result[0]


#get all tweets from the tempTweets table
def read_raw_statuses(cursor):
    cursor.execute('SELECT statusID, tweetText FROM tempTweets')
    return cursor.fetchall()


'''
===============================================================================
========================create table stuff=====================================
===============================================================================
'''
#create table for tweets from both streams
def create_temp_tweets_table(cursor):
    cursor.execute('CREATE TABLE tempTweets(timeSaved TIMESTAMP NOT NULL DEFAULT NOW(), createdAt VARCHAR (50) NOT NULL, sourceStream VARCHAR (20) NOT NULL, statusID VARCHAR (35) NOT NULL, userID VARCHAR (20) PRIMARY KEY, screenName VARCHAR (140) NOT NULL, tweetText VARCHAR (300) NOT NULL, numLikes INTEGER DEFAULT 0, numRetweets INTEGER DEFAULT 0)')
    print('Successfully created tempTweets table')


'''
==============================================================================
========================insert query stuff====================================
==============================================================================
'''
#insert row into tempFollowingTweets table
def insert_raw_tweets_table(cursor, createdAt, sourceStream, statusID, userID, screenName, tweetText, numLikes, numRetweets):
    cursor.execute('INSERT INTO tempTweets(createdAt, sourceStream, statusID, userID, screenName, tweetText) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (createdAt, sourceStream, statusID, userID, screenName, tweetText, numLikes, numRetweets))



'''
==============================================================================
======================drop tables/deletion queries=============================
==============================================================================
'''
#delete the tweet that matches the inputted string
def delete_query(cursor, tweet):
    cursor.execute('DELETE FROM tweets WHERE tweet = %s', (tweet,))


#drop a table. Needs specific table's name
def drop_table(cursor, table_name):
    cursor.execute('DROP TABLE %s', (table_name,))
    print('Successfully dropped ', table_name)
