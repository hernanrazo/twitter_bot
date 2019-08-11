import sqlalchemy
import db_connect

#check if table is empty. return 1 if yes, 0 if not
def is_empty(session):

    check_query = session.query(class_tweets.id).first()

    if not check_query:
        return 0
    else:
        return 1


#get tweet that matches the given id
def read_query(session, random_num):

    select_query = session.execute(text('SELECT tweet FROM tweets WHERE id=:num'), {'num':random_num})

    return select_query


#delete the tweet that matches the inputted string
def delete_query(session, tweet):

    delete_query = session.query(text('DELETE FROM tweets WHERE id=:tweet'), {'tweet':tweet})
