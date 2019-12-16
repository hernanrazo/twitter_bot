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


#grab a random tweet
def get_id(cursor):
    select_query = cursor.execute('SELECT id FROM tweets')
    result = cursor.fetchall()
    selected_id = random.choice(result)
    print(selected_id)
    return selected_id


#get tweet that matches the given id
def read_query(cursor, tweet_id):
    select_query = cursor.execute('SELECT tweet FROM tweets WHERE id = %s', (tweet_id,))
    result = cursor.fetchone()
    return result[0]


#delete the tweet that matches the inputted string
def delete_query(cursor, tweet):
    delete_query = cursor.execute('DELETE FROM tweets WHERE tweet = %s', (tweet,))


#create table for tweets coming from users that are followed
def create_temp_following_tweets_table(cursor):
    temp_raw_following_tweets_table = cursor.execute('CREATE TABLE tempFollowingTweets(timeSaved TIMESTAMP NOT NULL, createdAt VARCHAR (50) NOT NULL, id BIGINT PRIMARY KEY, screenName VARCHAR (140) NOT NULL, text VARCHAR (300) NOT NULL')
    print('Successfully created tempFollowingTweets')


#create table for tweets from general population
def create_temp_general_tweets_table(cursor):
    temp_raw_general_tweets_table = cursor.execute('CREATE TABLE tempGeneralTweets(timeSaved TIMESTAMP NOT NULL, createdAt VARCHAR (50) NOT NULL, id BIGINT PRIMARY KEY, screenName VARCHAR (140) NOT NULL, text VARCHAR (300) NOT NULL')
    print('Successfully created tempGeneralTweets')


#create table for tweets from general population
def create_temp_cleaned_tweets_table(cursor):
    temp_cleaned_tweets_table = cursor.execute('CREATE TABLE tempCleanedTweets(timeSaved TIMESTAMP NOT NULL, createdAt VARCHAR (50) NOT NULL, id BIGINT PRIMARY KEY, screenName VARCHAR (140) NOT NULL, clean_text VARCHAR (300) NOT NULL')
    print('Successfully created tempCleanedTweets')

#drop a table. Needs specific table's name
def drop_table(cursor, table_name):
    cursor.execute('DROP TABLE %s', (table_name))
    print('Successfully dropped +' table_name)
