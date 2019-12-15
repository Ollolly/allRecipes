# Constants for the project

# Website for scrapping
URL = 'https://www.allrecipes.com/'


# Scraping keys used in the module recipe_details.py
RECIPE_DETAILS = ['category', 'sub_category', 'url',
                  'author', 'review', 'summary', 'name', 'prep_time', 'calories',
                  'rating', 'image', 'directions', 'ingredients_description','ingredients_list']


# measurments tool used in the module recipe_details.py
MEASUREMENTS = ('cup','cupBars','cupcup','cupcups','cups','cupscup','cupscups','ounce','ouncescup',
                'pinch','pound','ripe','tablespoon','tablespoons','teaspoon','teaspooncup',
                'teaspooncups','teaspoons','teaspoonscup','teaspoonsounce','verycup')


# measurments tool used in the module recipe_details.py
INGREDIENTS = ('cucamber', 'pimento', 'wheat', 'asparagus', 'garlic', 'oil', 'cider', 'maraschino',
               'cherries', 'pecan', 'raspberries', 'rib', 'olive', 'sugar', 'baking powder',
               'cayenne', 'raisins', 'spinach', 'celery', 'onion', 'anchovy', 'beer', 'tuna',
               'potato', 'beans','soy', 'pomegranate', 'vinaigrette', 'oregano', 'cranberries',
               'peach', 'Dijon', 'seaweed','butter', 'fish', 'liqueur', 'lemon', 'parsley',
               'pepper', 'sweet potato', 'hazelnuts', 'chickpeas', 'Cheddar', 'yeast', 'lime',
               'buckwheat', 'broccoli', 'salt', 'graham', 'seeds', 'wine', 'horseradish', 'cloves',
               'broth', 'mustard', 'almonds', 'cornbread', 'mascarpone', 'potatoes', 'apple',
               'peanut', 'duck', 'stalks', 'glutenfree', 'orange juice', 'coconut', 'pears',
               'rosemary', 'poultry', 'orange', 'pumpkin', 'halves', 'cheese', 'water', 'canola',
               'bonein', 'rum', 'sage', 'milk', 'gelatin', 'cocoa', 'strawberries', 'farina',
               'cherry', 'chicken', 'basil', 'hens', 'vanilla extract', 'seed', 'anise',
               'marshmallows', 'raspberry', 'grapes', 'lobster', 'goat cheese', 'alfalfa',
               'blackberry', 'sprouts', 'carrot', 'bourbon', 'vinegar', 'paprika', 'cereal', 'nuts',
               'jam', 'shallots', 'honey', 'yolk', 'chocolate', 'sauerkraut', 'leaf', 'greens',
               'peppermint', 'whiskey', 'tenderloin', 'eggnog', 'cucumbers', 'flour', 'beef',
               'kidney', 'cranberry', 'liver', 'oat', 'lettuce', 'margarine', 'banana', 'molasses',
               'walnut', 'feta', 'cinnamon', 'almond', 'salami', 'zest', 'rice', 'bread', 'soda',
               'avocado', 'mushroom', 'olive oil', 'Condensed milk', 'pudding', 'nutmeg', 'ham',
               'goose', 'corn', 'buttermilk', 'lemonlime', 'cornstarch', 'pork', 'ginger', 'yogurt',
               'beet', 'pecans', 'egg', 'Pudding', 'leaves', 'balsamic', 'mayonnaise', 'pineapple',
               'mandarin', 'bacon', 'brussels', 'crumbs', 'Parmesan', 'tomato', 'romaine', 'cream',
               'sesame', 'maple', 'blueberries', 'chips', 'turkey', 'curry', 'salmon')
