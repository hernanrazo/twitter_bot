import sqlalchemy
import db_connect

#check if table is empty. return 1 if yes, 0 if not
def is_empty(session):

    check = session.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = check.fetchall()
    return result


#get tweet that matches the given id
def read_query(session, random_num):

    result = session.execute('SELECT TWEET FROM TWEETS WHERE id = :num',{'num':random_num})
    query = result.fetchall()
    return query


#delete the tweet that matches the inputted string
def delete_query(session, tweet):

    delete_query = session.query(tweets_table).filter_by(tweets_table.tweets=tweet)
    delete_query.delete(synchronize session='evaluate')


