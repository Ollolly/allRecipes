from bs4 import BeautifulSoup
import requests
import logging
import recipe_details as rd
from config import URL, CATEGORY, SUBCATEGORY


def get_category_link(url, category):
    """ returns a link to a category/sub category """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    base = soup.find('div', id="insideScroll")
    links = {}
    for link in BeautifulSoup(str(base), 'lxml').findAll('a'):
        try:
            if link.span.text in category:
                links[link.span.text] = link['href']
        except ValueError:
            logging.error(f"Unrecognized category")
    return links[category]


def get_category_list(url):
    """ returns a list of all the valid options in category/subcategory """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    base = soup.find('div', id="insideScroll")
    category_list = []
    for link in BeautifulSoup(str(base), 'lxml').findAll('a'):
        try:
            category_list.append(link.span.text)
        except ValueError:
            logging.error(f"Unrecognized category")
    return category_list


def get_recipe_links(url):
    """ returns links to all recipes on webpage """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    links = soup.select('article.fixed-recipe-card div.grid-card-image-container a')
    links = [link['href'] for link in links if 'video' not in link['href']]
    return links


def write_cat_details_to_csv(cat, recipes):
    """ get recipe details for full category 'cat' and write to csv """
    logger = logging.getLogger(__name__)
    logger.info('Appending data to csv file')
    rep_data = rd.get_recipes_details(cat, recipes[cat])
    rd.write_data_to_csv(rep_data)