from bs4 import BeautifulSoup
import requests

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
    """ returns links to all recipes on webpage """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # find all recipes and extract their links
    links = soup.select('article.fixed-recipe-card div.grid-card-image-container a')
    links = [link['href'] for link in links if 'video' not in link['href']]
    return links


def write_cat(cat, recipes):
    rep_data = rd.get_recipes_details(cat, recipes[cat])
    rd.write_data_to_csv(rep_data)
