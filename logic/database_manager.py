import json


# write new product object into JSON file as a dictionary
def insertProduct(product):

    with open("./data/products.json", "r+") as file:
        all_products_dict = json.loads(file.read())      # read file and load current JSON contents in temp variable

        isInDatabase = checkProduct(product.getUrl(), all_products_dict["products"])
        if isInDatabase is True:
            return

        new_product = {"name": product.getName(), "start_price": product.getStartPrice(), "current_price": product.getCurrentPrice(),
                    "previous_price": product.getPreviousPrice(), "availability": product.getAvailability(),
                    "creation_date": product.getCreationDate(), "last_update": product.getLastUpdate(),
                    "is_lower_price": product.getIsLowerPrice(), "url": product.getUrl()}        # create a dictionary for new product
        
        file.seek(0)    # go to beginning of file
    
        all_products_dict["products"].append(new_product)    # add new product to product list

        json.dump(all_products_dict, file, indent = 4)   # write changes to JSON file


def checkProduct(url, all_products):
    isInDatabase = False

    for product in all_products:
        if product["url"] == url:
            isInDatabase = True

    return isInDatabase


# return a list of all tracked products within JSON file
def getAllProducts():
    products_dict = {}

    with open("./data/products.json", "r") as file:
        products_dict = json.loads(file.read())

    return products_dict["products"]    # return list of product items