# zumiez scraper
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import cv2

driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver')
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    base_url = 'https://www.zumiez.com/skate/skateboard-decks.html?p='
    page = 1 
    driver.get(base_url + str(page))

    i = 0
    images_found = True
    while images_found:
        images_found = False
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        for element1 in soup1.find_all('a', class_='product-image'):
            next_url = element1.get('href')
            driver.get(next_url)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            img_element = soup2.find('source', attrs={'media':'(min-width: 641px)'})
            if img_element is not None:
                srcset = str(img_element.get('srcset'))
                img_url = srcset[srcset.find(',') + 1:-3]
                images_found = True

                # download img; add padding on left and right to make square; resize to 512x512
                urlretrieve(img_url, f'/tmp/z_{i}.jpg')
                img = cv2.imread(f'/tmp/z_{i}.jpg')
                h, w = img.shape[:2]
                padded_img = cv2.copyMakeBorder(img, 0, 0, int((h - w)/2), int((h - w)/2), cv2.BORDER_REPLICATE)
                resized_img = cv2.resize(padded_img, (512, 512))
                cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/z_decks/z_{i}.png', resized_img)
                i += 1
        page += 1
        driver.get(base_url + str(page))

finally:
    driver.quit()