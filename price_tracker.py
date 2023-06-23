from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import sys
from product import Product

# Main function
def main():
    driver = createWebDriver()
    url = "https://www.amazon.ca/TRESemm%C3%A9-Botanique-Replenish-formulated-TechnologyTM/dp/B0BS763BBP/ref=sr_1_5?keywords=shampoo&qid=1687395876&sr=8-5"
    navigateToURL(driver, url)
    product_tuple = scrapeProductInfo(driver)   # tuple of strings about product info (name, price, availability)
    product_obj = Product(product_tuple[0], product_tuple[1], product_tuple[2])     # create new Product object using tuple
    print(product_obj)

    # page_html = (driver.page_source).encode("utf-8", "ignore")

    # quit web driver
    driver.quit()

# Initialize options and service for chrome web driver, and then create it
def createWebDriver():
    options = Options()

    # Enable headless mode for options, so browser window does not appear in GUI
    options.add_argument("--headless=new")
    
    # Enable incognito mode for browser
    options.add_argument("--incognito")

    # Ignore certificate errors
    options.add_argument("--ignore-certificate-errors")
    
    # Create instance for Chrome web driver
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    return driver

# Go to URL in browser
def navigateToURL(driver, url):
    driver.get(url)

# User CLI
def runInterface():
    print("\nWelcome to Amazon Price Tracker!\n")
    print("\nEnter 'o' to see the options menu\n")
    
    while True:
        input = sys.stdin()

        if (input == "o"):
            print("\n|-------------------------------------------------- OPTIONS --------------------------------------------------|\n")
            print("1) Enter 'list' to see the list of all products currently being tracked\n")
            print("2) Enter 'new [URL]' to start tracking a product (i.e.: 'new https://www.amazon.ca/fire-tv-40-inch)\n")
            print("3) Enter 'remove [list number]' to remove a product from the list of tracked products\n")
            print("4) Enter 'exit' to close the program\n")

# search through the html DOM and extract product information
def scrapeProductInfo(driver):
    try:

        # get the name
        name = findProductName(driver)

        # get the price
        price = findProductPrice(driver)

        # get the availability
        availability = findProductAvailability(driver)
        
        string_tuple = (name, price, availability)

    # failed to find all product details; throw exception
    except:
        print("\nCould NOT find the name and/or price for the product. The product will not be added to the tracking list. Please try again with a different URL.\n")

    return string_tuple

# find the product's price
def findProductPrice(driver):
    price = ""
    # first, try finding price for regular products
    try:
        parent_div = driver.find_element(By.ID, "corePrice_feature_div")
        price = parent_div.find_element(By.CLASS_NAME, "a-offscreen").get_attribute("textContent")
        # currency = (parent_div.find_element(By.CLASS_NAME, "a-price-symbol")).get_attribute("textContent")
        # price_whole = (parent_div.find_element(By.CLASS_NAME, "a-price-whole")).get_attribute("textContent")
        # price_fraction = (parent_div.find_element(By.CLASS_NAME, "a-price-fraction")).get_attribute("textContent")
        # price = currency + price_whole + price_fraction

    # if the above fails, the product is probably a book; search for different IDs
    except NoSuchElementException:
        try:
            price = (driver.find_element(By.ID, "kindle-price")).get_attribute("textContent")   # kindle edition
        except:
            price = (driver.find_element(By.ID, "price")).get_attribute("textContent")  # paperback
            raise Exception
    
    # all attempts to find price have failed; throw exception
    except Exception:
        print("\nFailed to find the price of the product.\n")
        raise Exception
    
    finally:
        price = price.strip()
        return price

# find the product's name
def findProductName(driver):
    name = ""
    try:
        name = (driver.find_element(By.ID, "productTitle")).text
    except:
        print("\nFailed to find the name of the product.\n")
        raise Exception
    finally:
        name = name.strip()
        return name

# find the product's availability (in stock, or out of stock)
def findProductAvailability(driver):
    availability = "unknown"
    try:
        availability = (driver.find_element(By.ID, "availability")).get_attribute("textContent")
    except:
        print("\nFailed to find the availability for the product.\n")
    finally:
        availability = availability.strip()
        return availability

# Run the main function if file is not imported as module
if __name__=="__main__":
    main()