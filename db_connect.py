import psycopg2
import logging
from pprint import pprint

'''
everything pertaining to the database.
Code includes setting up initial connection and
setting up queries to read and delete from
database
name, user, host, port, password
'''

logger = logging.getLogger()


def get_connection():

    DB_NAME = os.environ['DATABASE_NAME']
    DB_USER = os.environ['DATABASE_USER']
    DB_HOST = os.environ['DATABASE_HOST']
    DB_PASSWORD = os.environ['DATABASE_PASSWORD']
    DB_URI = os.environ['DATABASE_URI']
    PORT = os.environ['5432']
    try:
        conn = psycopg2.connect("dbname=DB_NAME user=DB_USER host=DB_HOST password=DB_PASSWORD")
    except:

        logger.error('Error connecting to database')

    logger.info('Successfully connected to database')

    return conn
