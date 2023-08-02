import json


# write new product object into JSON file as a dictionary
def insertProduct(product):

    with open("./data/products.json", "r+") as file:
        all_products_dict = json.loads(file.read())         # read file and load current JSON content
        all_products_list = all_products_dict["products"]   # list of dictionaries (one product = one dict)
        
        isInDatabase = checkDuplicateProduct(product.getUrl(), all_products_list)
        if isInDatabase is True:
            return
        
        lastId = findLastId(all_products_list) + 1

        new_product = {"id": lastId, "name": product.getName(), "start_price": product.getStartPrice(), "current_price": product.getCurrentPrice(),
                    "previous_price": product.getPreviousPrice(), "availability": product.getAvailability(),
                    "creation_date": product.getCreationDate(), "last_update": product.getLastUpdate(),
                    "is_lower_price": product.getIsLowerPrice(), "url": product.getUrl()}        # create a dictionary for new product
        
        file.seek(0)    # go to beginning of file
    
        all_products_dict["products"].append(new_product)    # add new product to product list

        json.dump(all_products_dict, file, indent = 4)   # write changes to JSON file


# check to see if product already exists in list
def checkDuplicateProduct(url, all_products):
    isInDatabase = False

    for product in all_products:
        if product["url"] == url:
            isInDatabase = True
            break

    return isInDatabase


# find the ID of the last product
def findLastId(all_products):
    lastId = 0
    size = len(all_products)

    if size > 0:
        lastProduct = all_products[size-1]
        lastId = lastProduct["id"]

    return lastId


# return a list of all tracked products within JSON file
def getAllProducts():
    products_dict = {}

    with open("./data/products.json", "r") as file:
        products_dict = json.loads(file.read())

    return products_dict["products"]    # return list of product items