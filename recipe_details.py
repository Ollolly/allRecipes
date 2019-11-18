import requests
import bs4
from collections import defaultdict
import csv


CATEGORIES = ['sub_category', 'url', 'author', 'review', 'summary', 'name', 'rating', 'image', 'prep_time',
              'calories', 'pieces']


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

        # extracting the author data
        result = soup.select('span[itemprop="author"]')
        recipes_data[i]['author'] = None
        if result is not None:
            try:
                s_author = result[0]
                author = s_author.text
                recipes_data[i]['author'] = author
            except IndexError or TypeError:
                pass

        # extracting number of reviews
        result = soup.select('span[class="review-count"]')
        recipes_data[i]['review'] = None
        if result is not None:
            try:
                s_review = result[0]
                review = s_review.text
                recipes_data[i]['review'] = review
            except IndexError or TypeError:
                pass

        # extracting the summary data
        result = soup.select('div[itemprop="description"]')
        recipes_data[i]['summary'] = None
        if result is not None:
            try:
                s_summary = result[0]
                summary = s_summary.text
                recipes_data[i]['summary'] = summary
            except IndexError or TypeError:
                pass

        # extracting the recipe name
        result = soup.select('h1[class="recipe-summary__h1"]')
        recipes_data[i]['name'] = None
        if result is not None:
            try:
                s_name = result[0]
                name = s_name.text
                recipes_data[i]['name'] = name
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

        # extracting the preparation time
        result = soup.select('span[aria-label="Ready in 50 Minutes"]')
        recipes_data[i]['prep_time'] = None
        if result is not None:
            try:
                s_prep_time = result[0]
                prep_time = s_prep_time.text
                recipes_data[i]['prep_time'] = prep_time
            except IndexError or TypeError:
                pass

        # extractiong the calories data
        result = soup.select('span[class="calorie-count"]')
        recipes_data[i]['calories'] = None
        if result is not None:
            try:
                s_calorie = result[0]
                calorie = s_calorie.text
                recipes_data[i]['calories'] = calorie
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

    return recipes_data


def write_data_to_csv(recipes_data):
    """ Appending the 'recepies_data' dictionary to csv file"""
    with open(r'recipes_details.csv', 'a', newline='') as csv_recipes_today:
        csv_writer = csv.writer(csv_recipes_today)
        headers = CATEGORIES
        csv_writer.writerow(headers)
        for key,row in recipes_data.items():
            csv_writer.writerow(row.values())
