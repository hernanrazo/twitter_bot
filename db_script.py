import sqlalchemy
import db_connect

<<<<<<< HEAD
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
=======

def is_empty(conn):

    check = conn.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = check.fetchall()

    return result


def read_query(conn, random_num):

    result = conn.execute("SELECT TWEET FROM TWEETS WHERE id = :num",{'num':random_num})

    query = result.fetchall()

    return query


def delete_query(conn, random_num):

    result = conn.execute('DELETE tweet FROM tweets WHERE id = :num', {'num': random_num})



>>>>>>> heroku/origin


