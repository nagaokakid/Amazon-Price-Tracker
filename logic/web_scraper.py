from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from logic import product
from logic import exception

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
    try:
        navigateToURL(driver, url)
        product_tuple = findProductInfo(driver)   # tuple of strings about product info (name, price, availability)
        product_obj = product.Product(product_tuple[0], product_tuple[1], product_tuple[2])     # create new Product object using tuple
    except Exception as e:
        raise e
    
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
    except Exception as e:
        print("\nMissing information. The product will not be added to the tracking list. Please try again with a different URL.\n")
        raise e

    return string_tuple

# find the product's price
def findProductPrice(driver):
    price = ""

    # first approach; search for most common div
    try:
        parent_div = driver.find_element(By.ID, "corePrice_feature_div")
        price = parent_div.find_element(By.CLASS_NAME, "a-offscreen").get_attribute("textContent")
        return price.strip()
    except NoSuchElementException:
        pass

    # second approach; search for desktop div
    try:
        parent_div = driver.find_element(By.ID, "corePrice_desktop")
        price = parent_div.find_element(By.CLASS_NAME, "a-offscreen").get_attribute("textContent")
        return price.strip()
    except NoSuchElementException:
        pass

    # if we reach here, the product is most likely a book...
    # third approach; search for kindle-related div
    try:
        price = (driver.find_element(By.ID, "kindle-price")).get_attribute("textContent")   # kindle edition
        return price.strip()
    except NoSuchElementException:
        pass
    
    # last approach; search for paperback-related div
    try:
        price = (driver.find_element(By.ID, "price")).get_attribute("textContent")  # paperback
        return price.strip()
    except:
        print("\nFailed to find the price of the product.\n")
        raise exception.NoProductPriceFound


# find the product's name
def findProductName(driver):
    name = ""
    
    try:
        name = (driver.find_element(By.ID, "productTitle")).text
        return name.strip()
    except:
        print("\nFailed to find the name of the product.\n")
        raise exception.NoProductNameFound


# find the product's availability (in stock, or out of stock)
def findProductAvailability(driver):
    availability = "unknown"
    
    try:
        availability = (driver.find_element(By.ID, "availability")).get_attribute("textContent")
        availability = availability.strip()
    except:
        print("\nFailed to find the availability for the product.\n")
    
    return availability