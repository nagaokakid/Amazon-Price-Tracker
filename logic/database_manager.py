import json


# write new product object into JSON file as a dictionary
def insertProduct(product):

    with open("./data/products.json", "r+") as file:
        all_products = json.loads(file.read())      # read file and load current JSON contents in temp variable
    
        new_product = {"name": product.getName(), "start_price": product.getStartPrice(), "current_price": product.getCurrentPrice(),
                    "previous_price": product.getPreviousPrice(), "availability": product.getAvailability(),
                    "creation_date": product.getCreationDate(), "last_update": product.getLastUpdate(),
                    "is_lower_price": product.getIsLowerPrice()}        # create a dictionary for new product
        
        file.seek(0)    # go to beginning of file
    
        all_products["products"].append(new_product)    # add new product to product list

        json.dump(all_products, file, indent = 4)   # write changes to JSON file


# return a list of all tracked products within JSON file
def getAllProducts():
    products_dict = {}

    with open("./data/products.json", "r") as file:
        products_dict = json.loads(file.read())

    return products_dict["products"]    # return list of product items