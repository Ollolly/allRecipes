from db import connect_db


def calories_query(min_cal, max_cal):
    """ retrieve recipes according to specified range of calories
     :param min_cal, max_cal as specified by the user
     :return recipes name and their urls which have calories value in the specified range
     """
    db, cursor = connect_db()
    cursor.execute(f"select name,url from recipes where calories between {min_cal} and {max_cal}")
    cursor.close()
    db.close()

def rating_query(min_rating, max_rating):
    """ retrieve recipes according to specified range of calories
    :param  min_rating, max_rating as specified by the user
    :return recipes name and their urls which have rating value in the specified range
    """
    db, cursor = connect_db()
    cursor.execute(f"select name,url from recipes where calories between {min_rating} and {max_rating}")
    cursor.close()
    db.close()

def prep_query(min_time, max_time):
    """ retrieve recipes according to specified range of preparation_time
    :param  min_time, max_time (in minutes) as specified by the user
    :return recipes name and their urls which have preparation time in the specified range
    """
    db, cursor = connect_db()
    cursor.execute(f"select name,url from recipes where calories between {min_time} and {max_time}")
    cursor.close()
    db.close()

def recipe_by_ingredient(ingredient_name):
    """ retrieve recipes according to specified ingredient from the scraped data as well as
    from data extracted from external api
    :param  ingredient_name as specified by the user
    :return recipes name and their urls which contains the specified ingredient
    """
    db, cursor = connect_db()
    cursor.execute(f"""select rec.name as recipe_name, rec.url as url, rec.image as recipe_image  from recipes rec
                    inner join recipe_ingredients re_ing on rec.id =re_ing.recipe_id
                    inner join ingredients ing on ing.id = re_ing.ingd_id
                    where ing.name = {ingredient_name}
                    union
                    select api.recipe_name, api.url as recipe_url, api.image as recipe_image from api_data api
                    inner join ingredients ing on ing.id=api.ingd_id
                    where ing.name={ingredient_name}""")
    cursor.close()
    db.close()

def recipe_by_ingredient(ingredient_name):
    """ retrieve Dietary values of a specified ingredient from data extracted from an external api
    :param  ingredient_name as specified by the user
    :return ingredient name and its Dietary values (enerc_kcal, procnt, fat, chocdf)
    """
    db, cursor = connect_db()
    cursor.execute(f"""select name, enerc_kcal, procnt, fat, chocdf from nutrients nut
                    inner join ingredients ing on ing.id=nut.ingd_id
                    where ing.name = {ingredient_name}""")
    cursor.close()
    db.close()


def delete_db():
    """ Deletes a database """
    db, cursor = connect_db()
    cursor.execute(f"DROP DATABASE {DB_NAME}")
    cursor.close()
    db.close()
