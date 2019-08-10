import sqlalchemy
import db_connect

#check if table is empty. return 1 if yes, 0 if not
def is_empty(session):



#get tweet that matches the given id
def read_query(session, random_num):

    select_query = session.query(class_tweets).filter_by(class_tweets.id=random_num)
    return select_query


#delete the tweet that matches the inputted string
def delete_query(session, tweet):

    delete_query = session.query(tweets_table).filter_by(tweets_table.tweets=tweet)
    delete_query.delete(synchronize session='evaluate')


