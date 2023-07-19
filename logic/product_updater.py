from logic.web_scraper import *
import json

def updateProducts(driver):

    try:
    
        with open("./data/products.json", "r+") as file:
            all_products_dict = json.loads(file.read())             # root dictionary in JSON file
            all_products_list = all_products_dict["products"]       # list of dictionary objects

            for product in all_products_list:
                price_before_check = product["current_price"]
                url = product["url"]

                navigateToURL(driver, url)
                price_after_check = findProductPrice(driver)

                if price_after_check < price_before_check:      # if price has gone down, update the product
                    product["previous_price"] = price_before_check
                    product["current_price"] = price_after_check
                    product["is_lower_price"] = True
            
            json.dump(all_products_dict, file, indent = 4)   # write changes to JSON file
    
    except Exception as e:
        raise e
