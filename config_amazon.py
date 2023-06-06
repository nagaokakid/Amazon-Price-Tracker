from selenium import webdriver

DIRECTORY = "reports"
NAME = ""
CURRENCY = "$"
MIN_PRICE = ""
MAX_PRICE = ""
FILTERS = {"min": MIN_PRICE, "max": MAX_PRICE}
BASE_URL = "http://www.amazon.ca"

def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)

def get_web_driver_options():
    return webdriver.ChromeOptions()

def set_ignore_certificate_error(options):
    options.add_argument("--ignore-certificate-errors")

def set_incognito_mode(options):
    options.add_argument("--incognito")



