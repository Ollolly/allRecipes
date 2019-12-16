"""
This module scraps given web links and handles extracted data from it:
     - extracted recipe details
     - writes recipe data to csv file
 """

from collections import defaultdict
import requests
import bs4
import os
import re
import logging
import csv
import numpy as np
from constants import MEASUREMENTS, RECIPE_DETAILS, INGREDIENTS
from config import FILENAME


def get_recipe_details(url):
    """ Extract recipe details from link
        Parameters:
        url (string) : url to scrap
        Returns:
        dict : recipe details
    """
    recipe_data = defaultdict(None)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "lxml")
    attribute_val = {'author': 'span[itemprop="author"]', 'review': 'span[class="review-count"]',
                     'summary': 'div[itemprop="description"]', 'name': 'h1[class="recipe-summary__h1"]',
                     'prep_time': 'span[class="ready-in-time"]', 'calories': 'span[class="calorie-count"]'}

    for attr, path in attribute_val.items():
        recipe_data[attr] = get_attribute(attr, path, soup)

    recipe_data['calories'] = convert_cal_to_int(recipe_data['calories'])
    recipe_data['review'] = convert_review_to_int(recipe_data['review'])
    recipe_data['prep_time'] = convert_prep_time_to_minutes(recipe_data['prep_time'])

    recipe_data['rating'] = get_rating(soup)
    recipe_data['image'] = get_image(soup)
    recipe_data['directions'] = get_directions(soup)
    recipe_data['ingredients_description'] = get_ingredients(soup)[0]
    recipe_data['ingredients_list'] = get_ingredients(soup)[1]
    return recipe_data


def get_attribute(attrib, path, data):
    """ extracting the recipe detail
        Parameters:
        attrib (string) : variable to extract from data
        path (string) : tag of attribute
        data (string) : scrapped data from website
        Returns:
        string : rating score
    """
    result = data.select(path)
    ret_val = None
    if result is not None:
        try:
            ret_val = result[0].text.strip()
        except IndexError or TypeError:
            logger = logging.getLogger(__name__)
            logger.warning(f'Failed to get {attrib} with path: {path}')
        finally:
            return ret_val


def get_rating(data):
    """ extracting the recipe rating
        Parameters:
        data (string) : scrapped data from website
        Returns:
        string : rating score
    """
    result = data.find('div', class_="rating-stars")
    ret_val = None
    if result is not None:
        try:
            ret_val = round(float(result['data-ratingstars']), 2)
        except IndexError or TypeError:
            logger = logging.getLogger(__name__)
            logger.warning(f'Failed to get rating')
        finally:
            return ret_val


def get_image(data):
    """ extracting the recipe image
        Parameters:
        data (string) : scrapped data from website
        Returns:
        string : link to image
    """
    result = data.find('img', class_="rec-photo")
    ret_val = None
    if result is not None:
        try:
            ret_val = result['src']
        except IndexError or TypeError:
            logger = logging.getLogger(__name__)
            logger.warning(f'Failed to get img')
        finally:
            return ret_val


def get_directions(data):
    """ extracting the recipe directions
        Parameters:
        data (string) : scrapped data from website
        Returns:
        string : directions list
    """
    result = data.findAll('span', class_="recipe-directions__list--item")
    ret_val = None
    if result is not None:
        directions = [tag.text.strip() for tag in result]
        ret_val = ' '.join(directions)
    return ret_val


def get_ingredients(data):
    """ extracting the recipe ingredients
        Parameters:
        data (string) : scrapped data from website
        Returns:
        string : ingredients list
    """
    result = data.findAll('span', class_="recipe-ingred_txt added")
    ret_val = None
    if result is not None:
        ingredients_description = [edit_ingredient(tag.text) for tag in result]
        ingredient_list = extract_ingredient([tag.text for tag in result])
    return [ingredients_description, ingredient_list]


def edit_ingredient(ingredient):
    """
    :param ingredient: text description of the ingredients as written in the site
    :return: list [quantity,ingredient_str] in which quantity is the measurment tool
    and its' quantity and ingredients is a string description of the recipes' ingredients
    """
    if len(ingredient.split()) == 2:
        return ingredient.split()[:2]
    elif np.array([mes not in ingredient for mes in MEASUREMENTS]).all():
        return ingredient
    else:
        try:
            mes = re.findall(r'([\d /]+) \w',ingredient)
            mes = mes[0]
            ind = ingredient.index(mes)
            quantity = ingredient[:ind+len(mes)]
            ingredient = ingredient[ind+len(mes):].split()
            quantity = quantity+' '+ingredient[0]
            ingredient_str = ' '.join(ingredient[1:])
            return [quantity, ingredient_str]
        except IndexError:
            return [None, ingredient]


def extract_ingredient(list_ingd):
    """
    gets ingredients description from get_ingredients, and return list
    of ingredients associated with the recipe
    :param : None
    :return: ingredients list
    """
    ingredient_list = []
    for ing in list_ingd:
        for ingd in INGREDIENTS:
            if ingd.lower() in ing.lower():
                ingredient_list.append(ingd)
    return ingredient_list


def convert_review_to_int(review):
    """ Gets review value as string and converts it to int
        Parameters:
        review (string) : review score
        Returns:
        int : review score
    """
    if review == '' or review is None:
        return None

    score = review.split()[0]
    mult = 1
    if score[-1] == 'k':
        mult = 1000
        score = score[:-1]
    num = None
    try:
        num = int(score) * mult
    except ValueError:
        logger = logging.getLogger(__name__)
        logger.warning(f'Failed to convert review score to int')

    return num


def convert_cal_to_int(calories):
    """ Gets calories value as string and converts it to int
        Parameters:
        calories (string) : amount of calories
        Returns:
        int : amount of calories
    """
    if calories is None:
        return None

    cal = None
    try:
        cal = int(re.findall(r'\d+', calories)[0])
    except ValueError:
        logger = logging.getLogger(__name__)
        logger.warning(f'Failed to convert calories to int')

    return cal


def convert_prep_time_to_minutes(prep_time):
    """ Gets preparation time value as string and converts it to minutes
        Parameters:
        prep_time (string) :  preparation time
        Returns:
        int : amount of minutes
    """
    if prep_time is None:
        return None

    minutes = None
    try:
        # TODO
        minutes = prep_time
    except ValueError:
        logger = logging.getLogger(__name__)
        logger.warning(f'Failed to convert preparation time to int')

    return minutes


def get_recipes_details(category, sub_category, urls):
    """ Extract recipe details for each link
        Parameters:
        category (strings) :  category
        sub_category (list of strings) : list of subcategories for scraping
        url (list of string): links for scraping
        Returns:
        list of dict : links to recipes, where key is category
    """
    recipes_data = []
    for url in urls:
        recipe = {'category': category, 'sub_category': sub_category, 'url': url}
        details = get_recipe_details(url)
        recipe.update(details)
        recipes_data.append(recipe)

    return recipes_data


def write_data_to_csv(recipes_data, filname, headers):
    """ Appending the data to csv file
        Parameters:
        recipes_data (list if dict): data to write to file
    """
    is_file_exists = False
    if os.path.exists(filname):
        is_file_exists = True

    with open(filname, 'a', newline='') as csv_output:
        csv_writer = csv.DictWriter(csv_output, headers)
        if not is_file_exists:
            csv_writer.writeheader()
        csv_writer.writerows(recipes_data)
