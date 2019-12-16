"""
This module contains the main function, and parse_arguments_advanced.
It executes the program from the main function, according to the specified arguments given by the user.
the input arguments are parsed by the parse_arguments_advanced function
"""

import logging
import logging.config
import argparse
import sys
import scrapping as sc
import api
import db
from constants import URL, INGREDIENTS, ING_DETAILS, RECIPE_DETAILS
from config import LOG_CONF, ING_FILENAME, REC_FILENAME



def parse_arguments_advanced():
    """ Processing and storing the arguments of the program
        returns an argparse.Nampespace object, depicting and store the input arguments
        according to the defined flags
    """
    parser = argparse.ArgumentParser(
        description="Script Description"
    )
    parser.add_argument("-l", "--list", help="""
                        output list of possible recipes categories if no further arguments is given
                        or list of possible recipes of sub-categories associated with the requested
                        category if the -c flag is specified with the category name
                        for example: '-l' will output list of optional categories.
                        '-lc cat1' will output all optional subcategories associated 
                        with the category cat1 """, action="store_true")

    parser.add_argument("-c", "--category", help="""receives one argument (category) after the
                        -l flag and outputs the list of sub categories associated 
                        with the specified category. for example: '-lc Cookies' will output the 
                        following list: ['Butter Cookies', 'Bar Cookies', .....]
                        """,    # TODO add a condition that this flag can not be independent
                        action="store")

    parser.add_argument("-g", "--get", help="""
                        scraping data of the requested category and subcategory and save it in a 
                        csv and sql data base. receives two arguments: category and sub-category 
                        Note: don't forget to add "" around category/subcategory of >=2 words.
                    
                        For example: -g Cookies "Butter Cookies" 
                        will output the recipes associated with Butter Cookies.
                        """, nargs='+')

    arguments = parser.parse_args()
    return arguments


def main():
    """ The main function executes the program """
    logging.config.fileConfig(LOG_CONF)
    logging.info('Writing ingredients info')
    info_ingredients = api.get_info_ingred()
    # print(info_ingredients)
    sc.write_data_to_csv(info_ingredients, ING_FILENAME, ING_DETAILS)
    #
    #
    logging.info('Scrapping category links')
    args = parse_arguments_advanced()
    # in case l is given alone
    if args.list and args.category is None:
        category_list = sc.get_category_list(URL)
        print(category_list)

    # in case -lc is given
    if not(args.list is None) and not(args.category is None):
        if len(args.list) != 1:
            cat = args.category
            cat_link = sc.get_category_links(URL, cat)
            sub_category_list = sc.get_category_list(cat_link[cat])
            print(sub_category_list)
        else:
            sys.exit("invalid input")

    # in case -g is given correctly(with category and aub-category)
    if not (args.get is None):
        if len(args.get) <= 1:
            sys.exit("invalid input")
        else:
            cat = args.get[0]
            sub_cat = args.get[1:]
            cat_link = sc.get_category_links(URL, cat)
            sub_cat_links = sc.get_category_links(cat_link[cat], sub_cat)
            recipes = {}
            for sub_cat, link in sub_cat_links.items():
                recipes[sub_cat] = sc.get_recipe_links(link)

            logging.debug(sub_cat_links)
            data = sc.scrap_data(cat, recipes)
            logging.debug(data)
            sc.write_data_to_csv(data, REC_FILENAME, RECIPE_DETAILS)
            db.write_data_to_db(data)


if __name__ == '__main__':
    main()
