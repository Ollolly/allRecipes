import requests
from selenium import webdriver
import bs4
from lxml import html
import os
from collections import defaultdict
import csv
import re


path = r'C:\Users\ravit\Documents\ITC\chromedriver.exe'
browser = webdriver.Chrome(path)
browser.maximize_window() #//For maximizing window
browser.implicitly_wait(20) #//gives an implicit wait for 20 seconds
browser.get('https://www.allrecipes.com/')
cookies = browser.find_element_by_xpath('//*[@id="insideScroll"]/ul/li[3]/a/img')
cookies.click()
butter = browser.find_element_by_xpath('//*[@id="insideScroll"]/ul/li[4]/a/img')
butter.click()
most_made_today = browser.find_element_by_class_name('list-recipes__carousel')
url_most_made_today=most_made_today.get_attribute('innerHTML')
print(url_most_made_today)
with open(r'url_most_made.html','w') as f:
    f.write(url_most_made_today)

with open(r'url_most_made.html','r') as f:
    page = f.read()

soup = bs4.BeautifulSoup(page,"lxml")
# soup=soup.prettify()

recipes=defaultdict(list)
recipe_data=soup.find_all('li',class_='list-recipes__recipe')

for i, recipe in enumerate(recipe_data):
    try:
        url_recipe = recipe.a['href'].split()[0]
        recipes[i] += [url_recipe]
    except TypeError:
        continue
recipes=dict(recipes)

csv_recipes_today = open(r'most_made_today_links.csv', 'w' ,newline='')
csv_writer= csv.writer(csv_recipes_today)
headers = ['Source']
csv_writer.writerow(headers)
for row in recipes.values():
    csv_writer.writerow(row)
csv_recipes_today.close()

with open(r'most_made_today_links.csv','r') as f:
    page = f.readlines()
urls=page[1:]
print(urls)

recipes_data = defaultdict(dict)
categories = ['url', 'author', 'review', 'summary', 'name', 'rating', 'image', 'prep_time', 'calories', 'pieces']
for i,url in enumerate(urls):
    try:
        file=requests.get(url)
        soup = bs4.BeautifulSoup(file.content,"lxml")
        recipes_data[i]['url'] = url
    except FileNotFound or TypeError:
        recipes_data[i]['url'] = None

    try:
        s_author = soup.select('span[itemprop="author"]')[0]
        author = s_author.text
        recipes_data[i]['author'] = author
    except TypeError:
        recipes_data[i]['author'] = None

    try:
        s_review = soup.select('span[class="review-count"]')[0]
        review = s_review.text
        recipes_data[i]['review'] = review
    except TypeError:
        recipes_data[i]['review'] = None

    try:
        s_summary= soup.select('div[itemprop="description"]')[0]
        summary = s_summary.text
        recipes_data[i]['summary'] = summary
    except TypeError:
        recipes_data[i]['summary'] = None

    try:
        s_name= soup.select('h1[class="recipe-summary__h1"]')[0]
        name = s_name.text
        recipes_data[i]['name'] = name
    except TypeError:
        recipes_data[i]['name'] = None

    try:
        s_rating = soup.find('div',class_="rating-stars")
        rating = s_rating['data-ratingstars']
        recipes_data[i]['rating'] = rating
    except TypeError:
        recipes_data[i]['rating'] = None

    try:
        s_image = soup.find('img',class_="rec-photo")
        image = s_image['src']
        recipes_data[i]['image'] = image
    except TypeError:
        recipes_data[i]['image'] = None

    try:
        s_prep_time= soup.select('span[aria-label="Ready in 50 Minutes"]')[0]
        prep_time=s_prep_time.text
        recipes_data[i]['prep_time'] = prep_time
    except:
        recipes_data[i]['prep_time'] = None

    try:
        s_calorie= soup.select('span[class="calorie-count"]')[0]
        calorie=s_calorie.text
        recipes_data[i]['calories'] = calorie
    except TypeError:
        recipes_data[i]['calories'] = None

    try:
        s_pieces= soup.find('span',class_="ng-binding")[0]
        pieces=s_pieces.text
        recipes_data[i]['pieces'] = pieces
    except TypeError:
        recipes_data[i]['pieces'] = None

print(recipes_data)

csv_recipes_today = open(r'most_made_today_01.csv', 'w' ,newline='')
csv_writer= csv.writer(csv_recipes_today)
# headers = categories
headers=recipes_data[0].keys()
csv_writer.writerow(headers)
for key,row in recipes_data.items():
    csv_writer.writerow(row.values())
csv_recipes_today.close()