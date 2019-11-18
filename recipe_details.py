import requests
import bs4
from collections import defaultdict
import csv


CATEGORIES = ['sub_category', 'url', 'author', 'review', 'summary', 'name', 'rating', 'image', 'prep_time',
              'calories', 'pieces', 'ingredients', 'directions']


def get_recipes_details(sub_category, urls):
    """ Extract details for each link from the variable 'urls' """
    recipes_data = defaultdict(dict)
    for i, url in enumerate(urls):
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, "lxml")
        recipes_data[i]['sub_category'] = sub_category

        # extracting the url data
        try:
            recipes_data[i]['url'] = url
        except IndexError or TypeError:
            recipes_data[i]['url'] = None

        # extracting data with the following pattern: soup.select(attribute_val[cat])
        attribute_val = {'author': 'span[itemprop="author"]', 'review': 'span[class="review-count"]',
                         'summary': 'div[itemprop="description"]', 'name': 'h1[class="recipe-summary__h1"]',
                         'prep_time': 'span[aria-label="Ready in 50 Minutes"]', 'calories':'span[class="calorie-count"]'}
        for cat in  attribute_val:
            result = soup.select(attribute_val[cat])
            recipes_data[i][cat] = None
            if result is not None:
                try:
                    recipes_data[i][cat] = result[0].text
                except IndexError or TypeError:
                    pass

            # extracting the recipe rating
        result = soup.find('div', class_="rating-stars")
        recipes_data[i]['rating'] = None
        if result is not None:
            try:
                s_rating = result
                rating = s_rating['data-ratingstars']
                recipes_data[i]['rating'] = rating
            except IndexError or TypeError:
                pass

        # extracting the recipe image
        result = soup.find('img', class_="rec-photo")
        recipes_data[i]['image'] = None
        if result is not None:
            try:
                s_image = result
                image = s_image['src']
                recipes_data[i]['image'] = image
            except IndexError or TypeError:
                pass

        # extracting the cookie quantity
        result = soup.find('span', class_="ng-binding")
        recipes_data[i]['pieces'] = None
        if result is not None:
            try:
                s_pieces = result[0]
                pieces = s_pieces.text
                recipes_data[i]['pieces'] = pieces
            except IndexError or TypeError:
                pass

        # extracting the cookie ingredients
        result = soup.findAll('span', class_="recipe-ingred_txt added")
        recipes_data[i]['ingredients'] = None
        if result is not None:
            ingredients = [tag.text for tag in result]
            recipes_data[i]['ingredients'] = ' '.join(ingredients)

        # extracting the cookie directions
        result = soup.findAll('span', class_="recipe-directions__list--item")
        recipes_data[i]['directions'] = None
        if result is not None:
            directions = [tag.text for tag in result]
            recipes_data[i]['directions'] = ' '.join(directions)

    return recipes_data



def write_data_to_csv(recipes_data):
    """ Appending the 'recepies_data' dictionary to csv file"""
    with open(r'recipes_details.csv', 'a', newline='') as csv_recipes_today:
        csv_writer = csv.writer(csv_recipes_today)
        headers = CATEGORIES
        csv_writer.writerow(headers)
        for key,row in recipes_data.items():
            csv_writer.writerow(row.values())
