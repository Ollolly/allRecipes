"""
This module handles the creation and management of the database:
     - creates new database if not exits
     - inserts data to database
     - delete database
 """

import logging
import mysql.connector as mysql

from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWD


def connect_db():
    """ connects to db, returns connection and cursor
        Returns:
        db: connection to db
        cursor: database cursor
    """
    db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)
    cursor = db.cursor()
    return db, cursor


def create_db():
    """ Creates database and tables if not exists """
    logger = logging.getLogger(__name__)
    logger.info("Create db and tables if not exists")
    db, cursor = connect_db()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.Error as err:
        db.close()
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating database: {err}"')
        raise Exception('DB error')

    try:
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS recipes (
                          id int PRIMARY KEY AUTO_INCREMENT,
                          name varchar(255),
                          category varchar(80),
                          sub_category varchar(80),
                          ingredients BLOB,
                          prep_time varchar(80),
                          calories int,
                          author varchar(100),
                          review int,
                          rating float,
                          url varchar(100),
                          image varchar(100),
                          summary BLOB,
                          directions BLOB
                        )""")
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        db.close()


def delete_db():
    """ Deletes a database """
    db, cursor = connect_db()
    cursor.execute(f"DROP DATABASE {DB_NAME}")
    db.close()


def insert_data_to_db(data):
    """ Insert data to database tables
        Parameters:
        data (list of dict): data to upload to database
    """
    db, cursor = connect_db()
    logger = logging.getLogger(__name__)
    logger.info("Starting to insert data into db")
    try:
        for i, record in enumerate(data):
            cursor.execute(f"USE {DB_NAME}")
            insert_query = """INSERT INTO recipes (name, category, sub_category, ingredients, prep_time, calories, 
                            author, review, rating, url, image, summary, directions) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            row = (record['name'], record['category'], record['sub_category'], record['ingredients'],
                   record['prep_time'], record['calories'], record['author'], record['review'], record['rating'],
                   record['url'], record['image'], record['summary'], record['directions'])
            cursor.execute(insert_query, row)

            if i % 10000 == 0:
                db.commit()
        db.commit()
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        db.close()


def write_data_to_db(data):
    """ Creates db and tales if not exists, and inserts data into it
        Parameters:
        data (list of dict): data to upload to database
    """
    create_db()
    insert_data_to_db(data)
