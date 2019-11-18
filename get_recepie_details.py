import requests
from selenium import webdriver
import bs4
from lxml import html
import os
from collections import defaultdict
import csv
import re

CATEGORIES = ['url', 'author', 'review', 'summary', 'name', 'rating', 'image', 'prep_time',
              'calories', 'pieces']


def get_recipes_details(urls):
    """ Extract details for each link from the variable 'urls' """
    recipes_data = defaultdict(dict)
    for i,url in enumerate(urls):

        # extracting the url data
        try:
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.content, "lxml")
            recipes_data[i]['url'] = url
        except IOError or TypeError:
            recipes_data[i]['url'] = None

        # extracting the author data
        try:
            s_author = soup.select('span[itemprop="author"]')[0]
            author = s_author.text
            recipes_data[i]['author'] = author
        except TypeError:
            recipes_data[i]['author'] = None

        # extracting number of reviews
        try:
            s_review = soup.select('span[class="review-count"]')[0]
            review = s_review.text
            recipes_data[i]['review'] = review
        except TypeError:
            recipes_data[i]['review'] = None

        # extracting the summary data
        try:
            s_summary= soup.select('div[itemprop="description"]')[0]
            summary = s_summary.text
            recipes_data[i]['summary'] = summary
        except TypeError:
            recipes_data[i]['summary'] = None

        # extracting the recipe name
        try:
            s_name= soup.select('h1[class="recipe-summary__h1"]')[0]
            name = s_name.text
            recipes_data[i]['name'] = name
        except TypeError:
            recipes_data[i]['name'] = None

        # extracting the recipe rating
        try:
            s_rating = soup.find('div',class_="rating-stars")
            rating = s_rating['data-ratingstars']
            recipes_data[i]['rating'] = rating
        except TypeError:
            recipes_data[i]['rating'] = None

        # extracting the recipe image
        try:
            s_image = soup.find('img',class_="rec-photo")
            image = s_image['src']
            recipes_data[i]['image'] = image
        except TypeError:
            recipes_data[i]['image'] = None

        # extracting the preparation time
        try:
            s_prep_time= soup.select('span[aria-label="Ready in 50 Minutes"]')[0]
            prep_time=s_prep_time.text
            recipes_data[i]['prep_time'] = prep_time
        except:
            recipes_data[i]['prep_time'] = None

        # extractiong the calories data
        try:
            s_calorie= soup.select('span[class="calorie-count"]')[0]
            calorie=s_calorie.text
            recipes_data[i]['calories'] = calorie
        except TypeError:
            recipes_data[i]['calories'] = None

        # extracting the cookie quantity
        try:
            s_pieces= soup.find('span',class_="ng-binding")[0]
            pieces=s_pieces.text
            recipes_data[i]['pieces'] = pieces
        except TypeError:
            recipes_data[i]['pieces'] = None

    return recipes_data


def write_data_to_csv(recipes_data):
    """ Writing the 'recepies_data' dictionary to csv file """
    with open(r'most_made_today_01.csv', 'w' ,newline='') as csv_recipes_today:
        csv_writer= csv.writer(csv_recipes_today)
        headers = CATEGORIES
        csv_writer.writerow(headers)
        for key,row in recipes_data.items():
            csv_writer.writerow(row.values())
