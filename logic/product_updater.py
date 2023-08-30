from logic.web_scraper import *
import json

def updateProducts(driver):

    try:
    
        with open("./data/products.json", "r+") as file:
            all_products_dict = json.loads(file.read())             # root dictionary in JSON file
            all_products_list = all_products_dict["products"]       # list of dictionary objects

            if len(all_products_list) == 0:
                return

            for product in all_products_list:
                base_string_before_check = product["current_price"]            # find current price in JSON file
                price_string = base_string_before_check
                if isinstance(price_string, str):
                    price_string = price_string.replace("$", "")        # remove dollar sign
                    price_string = price_string.replace(",", "")        # remove commas
                price_before_check = float(price_string)
                
                url = product["url"]        # find current price via web browser
                navigateToURL(driver, url)                  
                base_string_after_check = findProductPrice(driver)
                price_string = base_string_after_check
                if isinstance(price_string, str):
                    price_string = price_string.replace("$", "")        # remove dollar sign
                    price_string = price_string.replace(",", "")        # remove commas
                price_after_check = float(price_string)

                if price_after_check < price_before_check:      # compare prices and update the product if needed
                    product["previous_price"] = base_string_before_check
                    product["current_price"] = base_string_after_check
                    product["is_lower_price"] = True

            all_products_dict["products"] = all_products_list
            file.seek(0)
            json.dump(all_products_dict, file, indent = 4)   # write changes to JSON file
    
    except Exception as e:
        raise e
