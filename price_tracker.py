from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.python.org")
time.sleep(5)
driver.close()

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self):
        pass
