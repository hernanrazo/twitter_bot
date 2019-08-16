import psycopg2

#check if table is empty. return 1 if yes, 0 if not
def is_empty(cursor):

    cursor.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = cursor.fetchone()

    while result is not None:
        print('check_query value: ' + str(result[1]))


    if check_query is None:
        return 0
    else:
        return 1


#get tweet that matches the given id
def read_query(cursor, random_num):

    select_query = cursor.execute('SELECT tweet FROM tweets WHERE id = %(num)d', {'num':random_num})

    return select_query


#delete the tweet that matches the inputted string
def delete_query(cursor, tweet):

    delete_query = cursor.execute('DELETE FROM tweets WHERE tweet = %(tweet)d', {'tweet':tweet})
