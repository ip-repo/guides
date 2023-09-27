import time
import requests
import ctypes
from selenium import webdriver  
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(executable_path="chromedriver", options=options)

driver.implicitly_wait(10)
driver.get("https://apod.nasa.gov/apod/astropix.html")
time.sleep(4)
image = driver.find_element(By.TAG_NAME, "img")
image.click()
time.sleep(4)


image_url = driver.current_url
time.sleep(1)
driver.quit()


image_type = "." + image_url.split(".")[-1]
image_request = requests.get(image_url)

#make sure to write a correct path to the directory
image_path = "C:\\full\\path\\image\\folder\\" + "picoftheday" + image_type


with open(image_path,"wb") as image_file:
    image_file.write(image_request.content)


ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
