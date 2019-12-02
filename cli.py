import scrapping as sc
from config import URL, CATEGORY

def main():
    link = sc.get_category_link(URL)[CATEGORY[0]]
    subcategory = sc.get_subcategory_links(link)

    recipes = {}
    for cat, link in subcategory.items():
        recipes[cat] = sc.get_recipe_links(link)

    # extract all data and write it to file
    # wrap the for loop as a func in scraping and call the function from the main
    for cat in recipes:
        sc.write_cat(cat, recipes)


if __name__ == '__main__':
    main()
