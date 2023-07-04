from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import sys
from product import Product

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

# close web driver when done with use
def closeWebDriver(driver):
    driver.quit()

# Go to URL in browser
def navigateToURL(driver, url):
    driver.get(url)

# scrape the web page of the given URL, then create a product object with corresponding details
def createProduct(driver, url):
    navigateToURL(driver, url)
    product_tuple = findProductInfo(driver)   # tuple of strings about product info (name, price, availability)
    product_obj = Product(product_tuple[0], product_tuple[1], product_tuple[2])     # create new Product object using tuple
    return product_obj

# search through the html DOM and extract product information
def findProductInfo(driver):
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