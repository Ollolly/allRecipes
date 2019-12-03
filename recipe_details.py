import requests
import bs4
from collections import defaultdict
import csv
import logging
import re

from config import RECIPE_DETAILS


def get_recipe_details(url):
    """ Extract recipe details from link """
    recipe_data = defaultdict(None)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "lxml")
    attribute_val = {'author': 'span[itemprop="author"]', 'review': 'span[class="review-count"]',
                     'summary': 'div[itemprop="description"]', 'name': 'h1[class="recipe-summary__h1"]',
                     'prep_time': 'span[class="ready-in-time"]', 'calories': 'span[class="calorie-count"]'}

    for attr, path in attribute_val.items():
        recipe_data[attr] = get_attribute(attr, path, soup)

    recipe_data['rating'] = get_rating(soup)
    recipe_data['img'] = get_image(soup)
    recipe_data['directions'] = get_directions(soup)
    recipe_data['ingredients'] = get_ingredients(soup)
    return recipe_data


def get_attribute(attrib, path, data):
    """ extracting the recipe detail """
    result = data.select(path)
    ret_val = None
    if result is not None:
        try:
            ret_val = result[0].text.strip()
            if attrib == 'calories':
                ret_val = int(re.findall(r'\d+', ret_val)[0])
        except IndexError or TypeError:
            logger = logging.getLogger(__name__)
            logger.warning(f'Failed to get {attrib} with path: {path}')
        finally:
            return ret_val


def get_rating(data):
    """ extracting the recipe rating """
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
    """ extracting the recipe image """
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
    """ extracting the recipe directions """
    result = data.findAll('span', class_="recipe-directions__list--item")
    ret_val = None
    if result is not None:
        directions = [tag.text.strip() for tag in result]
        ret_val = ' '.join(directions)
    return ret_val


def get_ingredients(data):
    """ extracting the recipe ingredients """
    result = data.findAll('span', class_="recipe-ingred_txt added")
    ret_val = None
    if result is not None:
        ingredients = [tag.text for tag in result]
        ret_val = ' '.join(ingredients)
    return ret_val


def get_recipes_details(category, sub_category, urls):
    """ Extract recipe details for each link from the variable 'urls' """
    recipes_data = defaultdict(dict)
    for i, url in enumerate(urls):
        recipes_data[i]['category'] = category
        recipes_data[i]['sub_category'] = sub_category
        recipes_data[i]['url'] = url
        details = get_recipe_details(url)
        recipes_data[i].update(details)

    return recipes_data


def write_data_to_csv(recipes_data):
    """ Appending the 'recepies_data' dictionary to csv file"""
    with open(r'recipes_details.csv', 'a', newline='') as csv_recipe:
        csv_writer = csv.writer(csv_recipe)
        headers = RECIPE_DETAILS
        csv_writer.writerow(headers)
        for row in recipes_data.values():
            csv_writer.writerow(row.values())
