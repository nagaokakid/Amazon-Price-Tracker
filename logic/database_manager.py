import json
from logic.exception import DatabaseError

# write new product object into JSON file as a dictionary
def insertProduct(product):

    try:
        with open("./data/products.json", "r+") as file:
            # read file and load current JSON content
            all_products_dict = json.loads(file.read())
            
            # list of dictionaries (one product = one dict)
            all_products_list = all_products_dict["products"]
            
            # if product already exists, cancel insertion attempt
            isInDatabase = checkDuplicateProduct(product.getUrl(), all_products_list)  
            if isInDatabase is True:
                return

            lastId = findHighestId(all_products_list) + 1      # get new highest ID

            new_product = {"id": lastId, "name": product.getName(), "start_price": product.getStartPrice(), "current_price": product.getCurrentPrice(),
                        "previous_price": product.getPreviousPrice(), "availability": product.getAvailability(),
                        "creation_date": product.getCreationDate(), "last_update": product.getLastUpdate(),
                        "is_lower_price": product.getIsLowerPrice(), "url": product.getUrl()}        # create a dictionary for new product

            file.seek(0)    # go to beginning of file

            # add new product to product list
            all_products_dict["products"].append(new_product)

            # write changes to JSON file
            json.dump(all_products_dict, file, indent=4)
    except:
        raise DatabaseError


# check to see if product already exists in list
def checkDuplicateProduct(url, all_products):
    isInDatabase = False

    for product in all_products:
        if product["url"] == url:
            isInDatabase = True
            break

    return isInDatabase


# find the ID of the last product
def findHighestId(all_products):
    lastId = 0

    for product in all_products:
        if product["id"] > lastId:
            lastId = product["id"]

    return lastId


# return a list of all tracked products within JSON file
def getAllProducts():
    try:
        products_dict = None

        with open("./data/products.json", "r") as file:
            products_dict = json.loads(file.read())

        return products_dict["products"]    # return list of product items
    except:
        raise DatabaseError


# delete product from JSON database
def deleteProduct(id):
    try:
        with open("./data/products.json", "r+") as file:
            # read file and load current JSON content
            all_products_dict = json.loads(file.read())
            # list of dictionaries (one product = one dict)
            all_products_list = all_products_dict["products"]
            new_dict = {"products": []}

            for index, product in enumerate(all_products_list):
                if product["id"] == id:
                    del all_products_list[index]
                    break

            new_dict["products"] = all_products_list
            file.seek(0)    # go to beginning of file
            json.dump(new_dict, file, indent=4)   # write changes to JSON file
            file.truncate()
    except:
        raise DatabaseError


# get the number of products in database
def getSize():
    try:
        with open("./data/products.json", "r") as file:
            all_products_dict = json.loads(file.read())
            all_products_list = all_products_dict["products"]
            size = len(all_products_list)
    except:
        raise DatabaseError

    return size 