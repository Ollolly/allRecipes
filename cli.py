import logging
import logging.config

import scrapping as sc
from config import URL, CATEGORY, LOG_CONF


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
    data = sc.scrap_data(CATEGORY[0], recipes)
    sc.write_data_to_csv(data)


if __name__ == '__main__':
    main()
