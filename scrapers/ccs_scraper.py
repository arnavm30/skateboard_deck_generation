# ccs scraper
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import cv2

driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver')
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    base_url = 'https://shop.ccs.com/skateboards/skateboard-decks/popsicle?order=name&p='
    page = 1
    driver.get(base_url + str(page))

    i = 0
    images_found = True
    while images_found:
        images_found = False
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        for element1 in soup1.find_all('a', class_='product-image', attrs={'itemprop':'url'}):
            next_url = element1.get('href')
            driver.get(next_url)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            img_element = soup2.find('a', class_='image-zoom', attrs={'href': re.compile(r'-1')})
            if img_element is not None:
                img_url = img_element.get('href')
                images_found = True

                # download img; add padding on left and right to make square; resize to 512x512
                urlretrieve(img_url, f'/tmp/ccs_{i}.jpg')
                img = cv2.imread(f'/tmp/ccs_{i}.jpg')
                h, w = img.shape[:2]
                padded_img = cv2.copyMakeBorder(img, 0, 0, int((h - w)/2), int((h - w)/2), cv2.BORDER_REPLICATE)
                resized_img = cv2.resize(padded_img, (512, 512))
                cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/ccs_decks/ccs_{i}.png', resized_img)
                i += 1
        page += 1
        driver.get(base_url + str(page))

finally:
    driver.quit()