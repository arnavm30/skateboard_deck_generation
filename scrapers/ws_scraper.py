# warehouse skateboards scraper
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import cv2

driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver')
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    driver.get('https://www.warehouseskateboards.com/skateboard-decks#class=1d&sort=title&pg=1&category=1539|')

    # more images load as you scroll, so keep scrolling until reach bottom
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5) # seconds between scrolls
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    # get nested data structure of home page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # iterate through structure for images
    # for each image: download and resize to 512x512 square
    i = 0
    for img_element in soup.find_all('a', class_='quickView'):
        img_url = img_element.get('href')
        urlretrieve(img_url, f'/tmp/deck_{i}.jpg')
        img = cv2.imread(f'/tmp/deck_{i}.jpg')
        resized_img = cv2.resize(img, (512, 512))
        cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/decks/ws_{i}.png', resized_img)
        i += 1

finally:
    driver.quit()