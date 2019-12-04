from bs4 import BeautifulSoup
import requests
import logging

import recipe_details as rd
from config import URL, CATEGORY, SUBCATEGORY


def get_category_link(url):
    """ returns a link to a category """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    base = soup.find('div', id="insideScroll")
    links = {}
    for link in BeautifulSoup(str(base), 'lxml').findAll('a'):
        if link.span.text in CATEGORY:
            links[link.span.text] = link['href']
    return links


def get_subcategory_links(url):
    """ returns a list of subcategory links """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    base = soup.find('div', id="insideScroll")
    sub_category_list = {}
    for link in BeautifulSoup(str(base), 'lxml').findAll('a'):
        if link.span.text in SUBCATEGORY:
            sub_category_list[link.span.text] = link['href']
    return sub_category_list


def get_recipe_links(url):
    """ returns links to all recipes on webpage
        Parameters:
        url (string): link for scraping
        Returns:
        list: list of links to recipes
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # find all recipes and extract their links
    links = soup.select('article.fixed-recipe-card div.grid-card-image-container a')
    links = [link['href'] for link in links if 'video' not in link['href']]
    return links


def scrap_data(category, subcategories_links):
    """ scraps recipe details for category and subcategories
        Parameters:
        category (string): category for scraping
        subcategories_links (dict): links for scraping, where subcategories is a key
        Returns:
        list of dict: where each dictionary contains data of one link
    """
    logger = logging.getLogger(__name__)
    rep_data = []
    for cat, links in subcategories_links.items():
        logger.info(f'Extracting data from category {category} , subcategory {cat}')
        data = rd.get_recipes_details(category, cat, links)
        rep_data.extend(data)
    return rep_data


def write_data_to_csv(data):
    """ get recipe details and write it to csv
        Parameters:
        data (list of dict): data to write to csv file
        Returns:
        list of dict: where each dictionary contains data of one link
    """
    logger = logging.getLogger(__name__)
    logger.info(f'Appending data to csv file')
    rd.write_data_to_csv(data)
