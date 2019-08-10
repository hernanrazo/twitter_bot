import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper

'''everything necessary to get database connection'''

class class_tweets(object):
    pass


def get_database():

    DB_URL = os.environ['DATABASE_URL']

    try:

        engine = create_engine(DB_URL, echo=True)
        metadata = MetaData(engine)
        tweets_table = Table('tweets', metadata, autoload=True)
        mapper(class_tweets, tweets)
        Session = sessionmaker(bind=engine)
        session = Session()

        print('Successfully connected to database')
        sys.stdout.flush()

        return session

    DB_URL = os.environ['DATABASE_URL']

    try:
        
        engine = create_engine(DB_URL)
        conn = engine.connect()

        print('Successfully connected to database')
        sys.stdout.flush()

        return conn

    except:

        sys.exit('Error: Cannot connect to database')
