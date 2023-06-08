from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import product

# Main function
def main():
    driver = createWebDriver()
    url = "https://www.amazon.ca/iRobot-Roomba-Wi-Fi-Connected-Vacuum/dp/B08C4JXBPF?ref_=Oct_DLandingS_D_3709f0ee_2&th=1"
    navigateToURL(driver, url)
    scrapeProductInfo(driver)

    # page_html = (driver.page_source).encode("utf-8", "ignore")

    driver.quit()

# Initialize options and service for chrome web driver
def createWebDriver():
    # Enable headless mode for options, so browser window does not appear in GUI
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1200")
    # Enable incognito mode for browser
    options.add_argument("--incognito")
    # Ignore certificate errors
    options.add_argument("--ignore-certificate-errors")
    
    # Create instance for Chrome web driver
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    return driver

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
    # try:
        # get the price
        price = getProductPrice(driver)

        # get the name
        name = getProductName(driver)

        # get the availability
        availability = getProductAvailability(driver)

        print(price + "\n" + name + "\n" + availability + "\n")



    # except:
        # print("\nERROR: Failed to find any product information for the given URL. Please ensure the correct URL is entered, corresponding to the product page on Amazon.\n")
        # sys.exit()  

# find the product's price
def getProductPrice(driver):
     currency = (driver.find_element(By.CLASS_NAME, "a-price-symbol")).get_attribute("textContent")
     price_whole = (driver.find_element(By.CLASS_NAME, "a-price-whole")).get_attribute("textContent")
     price_fraction = (driver.find_element(By.CLASS_NAME, "a-price-fraction")).get_attribute("textContent")
     price = currency + price_whole + price_fraction
     return price

# find the product's name
def getProductName(driver):
    name = (driver.find_element(By.ID, "productTitle")).text
    return name

# find the product's availability (in stock, or out of stock)
def getProductAvailability(driver):
    availability = (driver.find_element(By.ID, "availability")).text
    return availability

# Run the main function if file is not imported as module
if __name__=="__main__":
    main()