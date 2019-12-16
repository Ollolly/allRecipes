import requests
from pprint import pprint
from collections import defaultdict
from constants import INGREDIENTS, ING_DETAILS


def extract_extra(ing):
    """
    :param ing: Receive name of ingredient(ing)
    :return:  list of recipes associated with this ingredient, for each recipe the following data
    is provided: name, url
    """
    url = " http://www.recipepuppy.com/api/"
    l = []
    try:
        querystring = {"i": ing}
        headers = {
            'x-rapidapi-host': "recipe-puppy.p.rapidapi.com",
            'x-rapidapi-key': "56ae2ccbf4mshf55a5b55145a40ep1472b9jsn6a8637a31483"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        for recipe in data['results']:
            l.append({'title':recipe['title'], 'url':recipe['href'], 'img':recipe['thumbnail']})
        return l
    except:
        return


def extract_nutrients(ing):

    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
    try:
        querystring = {"ingr":ing}
        headers = {
            'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
            'x-rapidapi-key': "56ae2ccbf4mshf55a5b55145a40ep1472b9jsn6a8637a31483"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data =response.json()
        label = data['hints'][0]['food']['label']

        if label.lower().strip()==ing.lower().strip():
            ENERC_KCAL = data['hints'][0]['food']['nutrients']['ENERC_KCAL']
            FAT = data['hints'][0]['food']['nutrients']['FAT']
            PROCNT = data['hints'][0]['food']['nutrients']['PROCNT']
            CHOCDF = data['hints'][0]['food']['nutrients']['CHOCDF']
            return label, ENERC_KCAL, FAT, PROCNT, CHOCDF
    except:
        return

def get_info_ingred():
    ing_data=[]
    for ing in INGREDIENTS:
        ingred_data = {}
        try:
            if extract_nutrients(ing) is None:
                label, ENERC_KCAL, FAT, PROCNT, CHOCDF = None, None, None, None
            else:
                label, ENERC_KCAL, FAT, PROCNT, CHOCDF = extract_nutrients(ing)
            ingred_data['label']=ing
            ingred_data['ENERC_KCAL']=ENERC_KCAL
            ingred_data['FAT']=FAT
            ingred_data['PROCNT']=PROCNT
            ingred_data['CHOCDF']=CHOCDF


            if extract_extra(ing) is None:
                extra = []
            else:
                extra = extract_extra(ing)
            ingred_data['related_recipes']=extra
            ing_data.append(ingred_data)
        except:
            ing_data.append({})
    return ing_data


