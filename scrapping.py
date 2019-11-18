from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = 'https://www.allrecipes.com/'
SCROLL_DOWN = 4
CATEGORY = '#insideScroll > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)'  # Cookies
SUBCATEGORY = ['Butter Cookies']


def scroll_down(browser, number_of_scroll_downs):
    """ scrolls web page down """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    href = ''
    try:
        href = soup.select(CATEGORY)[0]['href']
    except IndexError:
        pass
    return href


def get_category_link(url):
    """ returns a link to a category """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    href = soup.select(CATEGORY)[0]['href']
    return href


def get_subcategory_links(url):
    """ returns a list of subcategory links """
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    base = soup.find('div', id="insideScroll")
    sub_category_list = []
    for link in BeautifulSoup(str(base), 'lxml').findAll('a'):
        if link.span.text in SUBCATEGORY:
            sub_category_list.append(link['href'])
    return sub_category_list


def get_recipe_links(url):
    """ returns links to all recipes on webpage """
    # browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    # browser.get(url)
    # time.sleep(1)
    # browser = scroll_down(browser, SCROLL_DOWN)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # find all recipes and extract their links
    links = soup.select('article.fixed-recipe-card div.grid-card-image-container a')
    links = [link['href'] for link in links]
    return links


def main():
    link = get_category_link(URL)
    subcategory = get_subcategory_links(link)
    recipes = []
    for cat in subcategory:
        recipes.append(get_recipe_links(cat))

    print(recipes)


if __name__ == '__main__':
    main()





