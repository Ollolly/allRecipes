import logging
import logging.config

import scrapping as sc
from config import URL, CATEGORY, LOG_CONF, SUBCATEGORY


def main():
    """ logger initialization """
    logging.config.fileConfig(LOG_CONF)
    logging.info('Scrapping category links')
    requested_category = [CATEGORY[0]]
    cat_link = sc.get_category_links(URL, requested_category)

    logging.info('Scrapping subcategory links')
    subcategory = sc.get_category_links(cat_link[requested_category[0]], SUBCATEGORY)

    recipes = {}
    for cat, link in subcategory.items():
        recipes[cat] = sc.get_recipe_links(link)

    # extract all data and write it to file
    data = sc.scrap_data(requested_category, recipes)
    sc.write_data_to_csv(data)


if __name__ == '__main__':
    main()

