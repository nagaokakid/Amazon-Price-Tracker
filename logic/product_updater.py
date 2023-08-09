from logic.web_scraper import *
import json
import string

def updateProducts(driver):

    try:
    
        with open("./data/products.json", "r+") as file:
            all_products_dict = json.loads(file.read())             # root dictionary in JSON file
            all_products_list = all_products_dict["products"]       # list of dictionary objects

            for product in all_products_list:
                price_string = product["current_price"]            # find current price in JSON file
                if isinstance(price_string, str):
                    price_string = price_string.replace("$", "")
                price_before_check = float(price_string)
                
                url = product["url"]        # find current price via web browser
                navigateToURL(driver, url)                  
                price_string = findProductPrice(driver)
                if isinstance(price_string, str):
                    price_string = price_string.replace("$", "")
                price_after_check = float(price_string)

                if price_after_check < price_before_check:      # compare prices and update the product if needed
                    product["previous_price"] = str(price_before_check)
                    product["current_price"] = str(price_after_check)
                    product["is_lower_price"] = True

            file.seek(0)
            json.dump(all_products_dict, file, indent = 4)   # write changes to JSON file
    
    except Exception as e:
        raise e
