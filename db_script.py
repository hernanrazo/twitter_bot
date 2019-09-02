import psycopg2
import random

#check if table is empty. return 1 if yes, 0 if not
def is_empty(cursor):

    cursor.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = cursor.fetchone()
    return int(result[0])

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
