import os
import sys
import logging
from sqlalchemy import create_engine


logger = logging.getLogger()


def get_connection():

    DB_URL = os.environ['DATABASE_URL']

    try:
        
        engine = create_engine(DB_URL)
        conn = engine.connect()

        print('Successfully connected to database')
        sys.stdout.flush()

        return conn

    except:

        sys.exit('Error: Cannot connect to database')
