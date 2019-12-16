"""
This module contains the main function, and parse_arguments_advanced.
It executes the program from the main function, according to the specified arguments given by the user.
the input arguments are parsed by the parse_arguments_advanced function
"""

import argparse
import scrapping as sc
import sys
import logging
from constants import URL
import db
import api
from config import REC_FILENAME, ING_FILENAME
from constants import RECIPE_DETAILS, ING_DETAILS


class Cli:

    def __init__(self):
        self.args = None
        self.logger = logging.getLogger(__name__)

    def parse_arguments_advanced(self):
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

        self.args = parser.parse_args()

    def args_handel(self):
        """ The function handles the arguments """
        self.logger.info(f'Starting to  handel arguments')
        # get current categories
        exist_cat = sc.get_category_list(URL)

        # in case l is given alone
        if self.args.list and self.args.category is None:
            return exist_cat

        # in case -lc is given
        if self.args.list is not None and self.args.category is not None:
            if len(self.args.list) != 1:
                if self.args.category not in exist_cat:
                    self.logger.error(f'Invalid input: category {self.args.category} not exists')
                    sys.exit("invalid input")

                cat_link = sc.get_category_links(URL, self.args.category)
                sub_category_list = sc.get_category_list(cat_link[self.args.category])
                return sub_category_list
            else:
                self.logger.error(f'Invalid input, args: -lc')
                sys.exit("invalid input")

        # in case -g is given correctly(with category and sub-category)
        if self.args.get is not None:
            if len(self.args.get) <= 1:
                self.logger.error(f'Invalid input, args: -g  requested '
                                  f'category {self.args.get[0]} requested subcategory {self.args.get[1:]}')
                sys.exit("invalid input")
            else:
                cat = self.args.get[0]
                if cat not in exist_cat:
                    self.logger.error(f'Invalid input: category {cat} not exists')
                    sys.exit("invalid input")

                cat_link = sc.get_category_links(URL, cat)
                exist_subcat = sc.get_category_list(cat_link[cat])
                sub_cat = self.args.get[1:]

                if set(sub_cat) - set(exist_subcat) != set():
                    self.logger.error(f'Invalid input: at least on of subcategories {sub_cat} not exists')
                    sys.exit("invalid input")

                cat_link = sc.get_category_links(URL, cat)
                sub_cat_links = sc.get_category_links(cat_link[cat], sub_cat)
                recipes = {}
                for sub_cat, link in sub_cat_links.items():
                    recipes[sub_cat] = sc.get_recipe_links(link)

                self.logger.debug(cat)
                self.logger.debug(sub_cat)
                data_sc = sc.scrap_data(cat, recipes)
                data_api = api.get_info_ingred()
                sc.write_data_to_csv(data_sc, REC_FILENAME, RECIPE_DETAILS)
                sc.write_data_to_csv(data_api, ING_FILENAME, ING_DETAILS)
                db.write_data_to_db(data_sc, data_api)
