# Constants for the project

# Website for scrapping
URL = 'https://www.allrecipes.com/'


# Scraping keys used in the module recipe_details.py
RECIPE_DETAILS = ['category', 'sub_category', 'url',
                  'author', 'review', 'summary', 'name', 'prep_time', 'calories',
                  'rating', 'image', 'directions', 'ingredients']

# Scraping keys used in the module api.py
ING_DETAILS = ['label', 'enerc_kcal', 'fat', 'procnt', 'carb', 'related_recipes']
RELATED_RECIPES = ['url', 'img']


# measurments tool used in the module recipe_details.py
MEASUREMENTS = ('cup', 'cupBars', 'cupcup', 'cupcups', 'cups', 'cupscup', 'cupscups', 'ounce', 'ouncescup',
                'pinch', 'pound', 'ripe', 'tablespoon', 'tablespoons', 'teaspoon', 'teaspooncup',
                'teaspooncups', 'teaspoons', 'teaspoonscup', 'teaspoonsounce', 'verycup')


MEASUREMENTS_DICT = {'cup': ['cup', 'cupBars', 'cupcup', 'cupcups', 'cups', 'cupscup', 'cupscups', 'ouncescup', 'verycup'],
                     'ounce': ['ounce', 'ounces', 'pinch'], 'pound': ['pound'],
                     'tablespoon': ['tablespoon', 'tablespoons'],
                     'teaspoon': ['teaspoon', 'teaspooncup', 'teaspooncups', 'teaspoons', 'teaspoonscup', 'teaspoonsounce'],
                     'item': ['item']}


# measurments tool used in the module recipe_details.py
INGREDIENTS = ('alfalfa', 'almond', 'almonds', 'anchovy', 'anise', 'apple', 'asparagus', 'avocado', 'bacon',
               'baking powder', 'balsamic', 'banana', 'basil', 'beans', 'beef', 'beer', 'beet', 'blackberry',
               'blueberries', 'bonein', 'bourbon', 'bread', 'brandy', 'broccoli', 'broth', 'brussels', 'buckwheat',
               'butter', 'buttermilk', 'canola', 'carrot', 'cayenne', 'celery', 'cereal', 'cheddar', 'cheese', 'cherries',
               'cherry', 'chicken', 'chickpeas', 'chips', 'chocolate', 'cider', 'cinnamon', 'cloves', 'cocoa',
               'coconut', 'condensed milk', 'corn', 'cornbread', 'cornstarch', 'cranberries', 'cranberry', 'cream',
               'crumbs', 'cucamber', 'cucumbers', 'curry', 'dijon', 'duck', 'egg', 'eggnog', 'farina', 'feta', 'fish',
               'flour', 'garlic', 'gelatin', 'ginger', 'glutenfree', 'goat cheese', 'goose', 'graham', 'grapes',
               'greens', 'halves', 'ham', 'hazelnuts', 'hens', 'honey', 'horseradish', 'jam', 'jimmies', 'kidney',
               'leaf', 'leaves', 'lemon', 'lemonlime', 'lettuce', 'lime', 'liqueur', 'liver', 'lobster', 'mandarin',
               'maple', 'maraschino', 'margarine', 'marshmallows', 'mascarpone', 'mayonnaise', 'milk', 'molasses',
               'mushroom', 'mustard', 'nutmeg', 'nuts', 'oat', 'oil', 'olive', 'olive oil', 'onion', 'orange',
               'orange juice', 'oregano', 'paprika', 'parmesan', 'parsley', 'peach', 'peanut', 'pears', 'pecan',
               'pecans', 'pepper', 'peppermint', 'pimento', 'pineapple', 'pomegranate', 'pork', 'potato', 'potatoes',
               'poultry', 'pudding', 'pudding', 'pumpkin', 'raisins', 'raspberries', 'raspberry', 'rib', 'rice',
               'romaine', 'rosemary', 'rum', 'sage', 'salami', 'salmon', 'salt', 'sauerkraut', 'seaweed', 'seed',
               'seeds', 'sesame', 'shallots', 'soda', 'soy', 'spinach', 'sprouts', 'stalks', 'strawberries', 'sugar',
               'sweet potato', 'tenderloin', 'tomato', 'tuna', 'turkey', 'vanilla extract', 'vinaigrette', 'vinegar',
               'walnut', 'water', 'wheat', 'whiskey', 'wine', 'yeast', 'yogurt', 'yolk', 'zest')

