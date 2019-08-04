import sqlalchemy
import db_connect


def is_empty(conn):

    check = conn.execute('SELECT SIGN(COUNT(*)) FROM tweets')
    result = check.fetchall()

    return result


def read_query(conn, random_num):

    result = conn.execute("SELECT TWEET FROM TWEETS WHERE id = :num",{'num':random_num})
    return result


def delete_query(conn, random_num):

    result = conn.execute('DELETE tweet FROM tweets WHERE id = :num', {'num': random_num})





