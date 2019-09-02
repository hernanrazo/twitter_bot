import psycopg2

#check if table is empty. return 1 if yes, 0 if not
def is_empty(cursor):

    cursor.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = cursor.fetchone()
    return int(result[0])


#get tweet that matches the given id
def read_query(cursor, random_num):

    select_query = cursor.execute('SELECT tweet FROM tweets WHERE id = %s', (random_num,))
    result = cursor.fetchone()

    while result is not None:
        return result[0]

#    else:
 #       print('trying again...')
  #      read_query(cursor, random_num)

#delete the tweet that matches the inputted string
def delete_query(cursor, tweet):

    delete_query = cursor.execute('DELETE FROM tweets WHERE tweet = %s', (tweet,))
