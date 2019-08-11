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
        print('1:Created engine')
        sys.stdout.flush()
        
        metadata = MetaData(engine)
        print('2:Created metadata')
        sys.stdout.flush()
        
        tweets_table = Table('tweets', metadata, autoload=True)
        print('3:Created tweets table')
        sys.stdout.flush()
        
        mapper(class_tweets, tweets)
        print('4:Created mapper')
        sys.stdout.flush()
        
        Session = sessionmaker(bind=engine)
        session = Session()
        print('Created session')
        
        sys.stdout.flush()
        print('Successfully connected to database')
        
        sys.stdout.flush()
        return session

    except:

        sys.exit('Error: Cannot connect to database')
