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
        metadata = MetaData()
        metadata.reflect(bind=engine)
        tweet_table = metadata.tables['tweets']
        return tweet_table

        print('Successfully connected to database')
        sys.stdout.flush()
        return tweet_table

    except:

        sys.exit('Error: Cannot connect to database')
