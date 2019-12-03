import logging
import logging.config

import scrapping as sc
from config import URL, CATEGORY, LOG_CONF


import recipe_details as rd


def main():
    """ logger initialization """
    logging.config.fileConfig(LOG_CONF)

    logging.info('Scrapping category links')
    link = sc.get_category_link(URL)[CATEGORY[0]]
    logging.info('Scrapping subcategory links')
    subcategory = sc.get_subcategory_links(link)

    recipes = {}
    for cat, link in subcategory.items():
        recipes[cat] = sc.get_recipe_links(link)

    # extract all data and write it to file
    # wrap the for loop as a func in scraping and call the function from the main
    for cat in recipes:
        sc.write_cat_details_to_csv('cookies', cat, recipes)

    # link = 'https://www.allrecipes.com/recipe/10192/russian-tea-cakes-i/?internalSource=hub%20recipe&referringId=15057&referringContentType=Recipe%20Hub&clickId=cardslot%208'
    # print(link)
    # recipe = rd.get_recipe_details(link)
    # print(recipe)
    #
    # for k, v in recipe.items():
    #     print(f'{k}: {v}', end='\n\n')


if __name__ == '__main__':
    main()
