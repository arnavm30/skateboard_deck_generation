# skate warehouse scraper
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import cv2

driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver')
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    driver.get('https://www.skatewarehouse.com/decks.html?view_all=true')
    soup1 = BeautifulSoup(driver.page_source, 'html.parser')

    i = 0
    for element1 in soup1.find_all('a', class_='image_wrap swatch_link'):
        next_url = element1.get('href')
        driver.get(next_url)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        img_element = soup2.find('img', class_='mainimage')
        if img_element is not None:
            img_url = img_element.get('srcset')[:-3]
            
            # download img; add padding on left and right to make square; resize to 512x512
            urlretrieve(img_url, f'/tmp/sw_{i}.jpg')
            img = cv2.imread(f'/tmp/sw_{i}.jpg')
            h, w = img.shape[:2]
            padded_img = cv2.copyMakeBorder(img, 0, 0, int((h - w)/2), int((h - w)/2), cv2.BORDER_REPLICATE)
            resized_img = cv2.resize(padded_img, (512, 512))
            cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/sw_decks/sw_{i}.png', resized_img)
            i += 1

finally:
    driver.quit()