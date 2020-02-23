"""
This module handles the creation and management of the database:
     - creates new database if not exits
     - inserts data to database
     - delete database
 """

import logging
import mysql.connector as mysql
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWD
from constants import INGREDIENTS


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
        # crete database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.Error as err:
        cursor.close()
        db.close()
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating database: {err}"')
        raise Exception('DB error')

    try:
        # crete tables
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS recipes (
                          id int PRIMARY KEY AUTO_INCREMENT,
                          name varchar(255),
                          category varchar(255),
                          sub_category varchar(255),
                          prep_time varchar(255),
                          calories int,
                          author varchar(255),
                          review int,
                          rating float,
                          url varchar(255),
                          image varchar(255),
                          summary BLOB,
                          directions BLOB
                        )""")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS ingredients (
                            id int PRIMARY KEY AUTO_INCREMENT,
                            name varchar(255)
                        )""")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS nutrients (
                            id int PRIMARY KEY AUTO_INCREMENT,
                            ingd_id int,
                            enerc_kcal float,
                            procnt float,
                            fat float,
                            carb float,
                            FOREIGN KEY (ingd_id) REFERENCES ingredients (id)
                        )""")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS recipe_ingredients (
                            id int PRIMARY KEY AUTO_INCREMENT,
                            recipe_id int,
                            ingd_id int,
                            quantity varchar(255),
                            measurement_tool varchar(255),
                            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
                            FOREIGN KEY (ingd_id) REFERENCES ingredients (id)
                        )""")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS api_data (
                            id int PRIMARY KEY AUTO_INCREMENT,
                            ingd_id int,
                            recipe_name varchar(255),
                            url varchar(255),
                            image varchar(255),
                            FOREIGN KEY (ingd_id) REFERENCES ingredients (id)
                        )""")

    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        cursor.close()
        db.close()


def delete_db():
    """ Deletes a database """
    db, cursor = connect_db()
    cursor.execute(f"DROP DATABASE {DB_NAME}")
    cursor.close()
    db.close()


def select_ingredients():
    """ selects ingredients from db and return them as dict
        return:
        dict: key is a ingredients, value it's id
    """
    db, cursor = connect_db()
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("SELECT * FROM ingredients")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    dct = {k: v for v, k in result}
    return dct


def insert_constant_data_to_db():
    """ Insert constant data from file "constants.py" to 'in'gredients' table """
    db, cursor = connect_db()
    logger = logging.getLogger(__name__)
    logger.info("Starting to insert data into db")
    try:
        for record in INGREDIENTS:
            cursor.execute(f"USE {DB_NAME}")
            insert_query = """INSERT INTO ingredients (name) VALUES (%s)"""
            cursor.execute(insert_query, (record,))

        db.commit()
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        cursor.close()
        db.close()


def insert_scrapped_data_to_db(data):
    """ Insert data to database tables
        Parameters:
        data (list of dict): data to upload to database
    """
    db, cursor = connect_db()
    logger = logging.getLogger(__name__)
    logger.info("Starting to insert data into db")
    try:
        ing = select_ingredients()
        cursor.execute(f"USE {DB_NAME}")
        for i, record in enumerate(data):
            insert_query_recipes = """INSERT INTO recipes (name, category, sub_category, prep_time, calories, 
                            author, review, rating, url, image, summary, directions) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            row_recipes = (record['name'], record['category'], record['sub_category'], record['prep_time'],
                           record['calories'], record['author'], record['review'], record['rating'],
                           record['url'], record['image'], record['summary'], record['directions'])
            cursor.execute(insert_query_recipes, row_recipes)

            insert_rec_ingd = """INSERT INTO recipe_ingredients (recipe_id, ingd_id, quantity, measurement_tool) 
                                VALUES (%s, %s, %s, %s)"""
            for item in record['ingredients']:
                quantity, measur, ingd = item
                ingd_id = ing[ingd]
                row_rec_ingd = (i + 1, ingd_id, quantity, measur)
                cursor.execute(insert_rec_ingd, row_rec_ingd)

            if i % 10000 == 0:
                db.commit()
        db.commit()
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        cursor.close()
        db.close()


def insert_api_data_to_db(data):
    """ Insert data to database tables
        Parameters:
        data (list of dict): data to upload to database
    """
    db, cursor = connect_db()
    logger = logging.getLogger(__name__)
    logger.info("Starting to insert data into db")
    try:
        ing = select_ingredients()
        cursor.execute(f"USE {DB_NAME}")
        for i, record in enumerate(data):
            ingd_id = ing[record['label']]
            insert_query_nutrients = """INSERT INTO nutrients (ingd_id, enerc_kcal, procnt, fat, carb) 
                                        VALUES (%s, %s, %s, %s, %s)"""
            row_nutr = (ingd_id, record['enerc_kcal'], record['procnt'], record['fat'], record['carb'])
            cursor.execute(insert_query_nutrients, row_nutr)
            insert_query_api_data = """INSERT INTO api_data (ingd_id, recipe_name, url, image) 
                                        VALUES (%s, %s, %s, %s)"""
            for subrec in record['related_recipes']:
                row_api_data = (ingd_id, subrec['title'], subrec['url'], subrec['img'])
                cursor.execute(insert_query_api_data, row_api_data)

            if i % 10000 == 0:
                db.commit()
        db.commit()
    except mysql.Error as err:
        logger = logging.getLogger(__name__)
        logger.error(f'Failed creating table: {err}"')
        raise Exception('DB error')
    finally:
        cursor.close()
        db.close()


def write_data_to_db(data_sc, data_api):
    """ Creates db and tales if not exists, and inserts data into it
        Parameters:
        data_sc (list of dict): data from scrapping to upload to database
        data_api (list of dict): data from api to upload to databases
    """
    create_db()
    insert_constant_data_to_db()
    insert_scrapped_data_to_db(data_sc)
    insert_api_data_to_db(data_api)
