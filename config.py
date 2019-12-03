# constants
# associated with the module recipe_details.py
RECIPE_DETAILS = ['category', 'sub_category', 'url',
                  'author', 'review', 'summary', 'name',  'prep_time', 'calories',
                  'rating', 'image', 'directions', 'ingredients']


# Website for scrapping
URL = 'https://www.allrecipes.com/'

# Path to CSV file name to save output data
FILENAME = 'recipes_details.csv'


# Path to logger configuration file
LOG_CONF = 'logging.conf'


# Database name
DB_NAME = 'allrecipes'

# Database connection params
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "sd"


# temporary (will be removed in version 2)

# associated with the module scrapping.py     
CATEGORY = ['Cookies']
SUBCATEGORY = ['Butter Cookies']
# SUBCATEGORY = ['Bar Cookies', 'Butter Cookies', 'Fruit Cookies']
