import logging
import mysql.connector as mysql

import recipe_details as rd
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWD, RECIPE_DETAILS


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
    for i, record in enumerate(data):
        cursor.execute("""INSERT INTO recipes VALUES (:cat, :sub_cat, :url, :author, :review, :summary, :name, 
                        :p_time, :cal, :rating, :img, :dir, :ingr)""",
                       {'cat': record['category'], 'sub_cat': record['sub_category'], 'url': record['url'],
                        'author': record['author'], 'review': record['review'], 'summary': record['summary'],
                        'name': record['name'], 'p_time': record['p_time'], 'cal': record['calories'],
                        'rating': record['rating'], 'img': record['image'], 'dir': record['directions'],
                        'ingr': record['ingredients']})
        if i % 10000 == 0:
            db.commit()
    db.commit()
    db.close()


def show_db():
    db, cursor = connect_db()
    cursor.execute(f"SHOW DATABASES")

    for i in cursor:
        print(i)
    db.close()


def write_data_to_db(category, subcategory, recipes):
    """ get recipe details for full category 'cat' and write to csv """
    logger = logging.getLogger(__name__)
    logger.info(f'Extracting data from category{category} , subcategory {subcategory}')
    rep_data = rd.get_recipes_details(category, subcategory, recipes)
    logger.info(f'Appending data to csv file: category{category} , subcategory {subcategory}')
    rd.write_data_to_csv(rep_data)


if __name__ == '__main__':
    create_db()

    # delete_db()
    show_db()
