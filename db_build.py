import logging
import mysql.connector as mysql

from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWD


def connect_db():
    """ connects to db, returns connection and cursor """
    db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)
    cursor = db.cursor()
    return db, cursor


def create_db():
    """ Creates database and tables if not exists """
    db, cursor = connect_db()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.Error as err:
        db.close()
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating database: {err}"')
        raise mysql.Error

    try:
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS recipes (
                          id int PRIMARY KEY AUTO_INCREMENT,
                          name varchar(255),
                          category varchar(80),
                          sub_category varchar(80),
                          ingredients varchar(255),
                          prep_time int,
                          calories int,
                          author varchar(100),
                          review int,
                          rating float,
                          url varchar(100),
                          image varchar(100),
                          summary varchar(255),
                          directions varchar(255)
                        )""")
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
    finally:
        db.close()


def delete_db():
    """ Deletes a database """
    db, cursor = connect_db()
    cursor.execute(f"DROP DATABASE {DB_NAME}")
    db.close()


def insert_data_to_db(data):
    """ Insert data from variable 'data' to database tables """
    db, cursor = connect_db()









def show_db():
    db, cursor = connect_db()
    cursor.execute(f"SHOW DATABASES")

    for i in cursor:
        print(i)
    db.close()


if __name__ == '__main__':
    create_db()

    # delete_db()
    show_db()
