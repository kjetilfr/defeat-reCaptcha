from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

import byeAllCaptcha

options = webdriver.FirefoxOptions()

options.add_argument("--window-size=1920,1080")

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")
# proxy_server_url = "139.144.24.46:8080"
# options.add_argument(f'--proxy-server={proxy_server_url}')
options.set_preference('intl.accept_languages', 'en-GB')

driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com/recaptcha/api2/demo")

#driver.get("file:///C:/Users/Kjetil/Desktop/test.htm")


def sleepRandomLow():
    return random.randint(1, 3)
time.sleep(2)


byeAllCaptcha.solveRecaptcha(driver)



#print(driver.find_element(By.ID, "rc-imageselect"))

# images = driver.find_elements(By.CSS_SELECTOR, "img")
#
# for image in images:
#     print(image.get_attribute("src"))



time.sleep(500)
