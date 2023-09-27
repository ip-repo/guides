<h2>Fetch nasa astronomy picture of the day and set it as wallpaper on Windows 10 </h2>

The goal is to navigate to <a href= "https://apod.nasa.gov/apod/astropix.html">nasa astronomy picture of the day </a> and download the image in order to set it has desktop wallpaper.

<h4>versions:</h4>

* python                    3.10.6
* selenium                  4.7.2
* requests                  2.28.1

First lets import libraries.
```python

import time
import requests
import ctypes
from selenium import webdriver  
from selenium.webdriver.common.by import By
```

Make sure you have a wevdriver.exe on your machine and that you know the path.<br> For this guide we will use chromium.<br>
If you dont have it you can download it from here <a href="https://chromedriver.chromium.org/downloads">https://chromedriver.chromium.org/downloads</a>.<br>
For this example the chromedriver.exe is placed on the same directory with the script.py file.

```
📁astronomy-potd
  chromedriver.exe
  script.py
```
Selenium usually launch a chromium window but for this script we dont need it and to achieve that we will use the option <b>"headless"</b>.<br>
Then we can create a Chrome object and give it the chromedriver.exe path and options.

```python
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(executable_path="chromedriver", options=options)

```
Then we navigate to the the pic of the day url and now we need to find the image and click on it.
```python
driver.implicitly_wait(10)
driver.get("https://apod.nasa.gov/apod/astropix.html")
time.sleep(4)
image = driver.find_element(By.TAG_NAME, "img")
image.click()
time.sleep(4)
```
The image will open in a new tab and we need is to save the new tab url because this going to be the url for requests.get(url=).<br>
Now we can close the driver and proceed to the next step.
```python

image_url = driver.current_url
time.sleep(1)
driver.quit()

```
Now we need to know the image type in order to save the image in a correct format.<br>
Then lets request the image
```python

image_type = "." + image_url.split(".")[-1]
image_request = requests.get(image_url)
image_path = "C:\\full\\path\\image\\folder\\" + "picoftheday" + image_type # enter the correct path to script folder
```
By this step we have response with the image (you can add tests for this step if you desire).<br>
Then we can save it as a image file.
```python

with open(image_path,"wb") as image_file:
    image_file.write(image_request.content)
```
Finally we will use ctypes to set the windows wallpaper with image_path saved earlier.
```python
ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
```

