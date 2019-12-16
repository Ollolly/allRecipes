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
            cal = data['hints'][0]['food']['nutrients']['ENERC_KCAL']
            fat = data['hints'][0]['food']['nutrients']['FAT']
            proteins = data['hints'][0]['food']['nutrients']['PROCNT']
            car = data['hints'][0]['food']['nutrients']['CHOCDF']
            return label, cal, fat, proteins, car
    except:
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to extract nutrients details for {label}")
        return

def get_info_ingred():
    logger = logging.getLogger(__name__)
    logger.info(f"Starting api scrapping")
    ing_data=[]
    for ing in INGREDIENTS:
        ingred_data = {}
        try:
            if extract_nutrients(ing) is None:
                label, cal, fat, proteins, car = None*5
            else:
                label, cal, fat, proteins, car = extract_nutrients(ing)
            ingred_data['label'] = ing
            ingred_data['cal'] = cal
            ingred_data['fat'] = fat
            ingred_data['proteins'] = proteins
            ingred_data['car'] = car


            if extract_extra(ing) is None:
                extra = []
            else:
                extra = extract_extra(ing)
            ingred_data['related_recipes']=extra
            ing_data.append(ingred_data)
        except:
            ing_data.append({})
    return ing_data


