import logging
import logging.config
import argparse
import scrapping as sc
from config import URL, CATEGORY, LOG_CONF


def parse_arguments_advanced(categories):

    categories_str = ', '. join(categories)
    parser = argparse.ArgumentParser(
        description="Script Description"
    )
    parser.add_argument("--l", help="""
                        output list of possible recipes categories if no further arguments is given
                        or list of possible recipes sub-categories of a requested category if the latter is given after the flag
                        for example: --r will output all optional categories and --r Cookies will output all optional subcategories associated with Cookies""")

    parser.add_argument("--g", help="""
                        Stands for a "get" mode. scraping data .... and return a relevant data regarding the requested category and subcategoy
                         recieves two arguments: category and sub-category 
                         according to the mode given by --s flag.
                        Note: 1. don't forget to add "" around category/subcategory of >=2 words.
                        2. This flag has to be followed by the --h flag
                    
                    
                        For example: --g Cookies "Butter Cookies"
                        """)

    parser.add_argument("--s", help="""
                        Indicates the requested format to save the data, 
                        choose "DB" to save the data in sql DB (divided to tables) or "csv" to save it as a whole in a csv file
                        default is to save it as a sql DB 
                        Valid categories are: {}""".format(categories_str)
                        , choices=['DB', 'csv'])
    # parser.add_argument("name", help="""
    #                     Indicates the name of the user we want to greet
    #                     """)
    #
    # parser.add_argument("--capitalize", help="Capitalizes the user's name",
    #                 action="store_true")
    arguments = parser.parse_args()
    return arguments


def main():
    """ logger initialization """
    logging.config.fileConfig(LOG_CONF)
    logging.info('Scrapping category links')
    categories = sc.get_category_list(URL)

    # args = parse_arguments_advanced(categories)
    # requested_category = args.category
    link = sc.get_category_link(URL, requested_category)
    logging.info('Scrapping subcategory links')
    subcategory = sc.get_category_links(link, subcategories)
    print(subcategory)
    # recipes = {}
    # for cat, link in subcategory.items():
    #     recipes[cat] = sc.get_recipe_links(link)
    #
    # # extract all data and write it to file
    # # wrap the for loop as a func in scraping and call the function from the main
    # for cat in recipes:
    #     sc.write_cat_details_to_csv(cat, recipes)



if __name__ == '__main__':
    main()
