from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


# Enable headless mode for options, so browser window does not appear in GUI
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1200")

# Initialize web driver for Chrome
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Navigate to URL
driver.get("https://www.python.org")
page_html = (driver.page_source).encode("utf-8", "ignore")
print(page_html)

# Shut down web driver
driver.quit()
