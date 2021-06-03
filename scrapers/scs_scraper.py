# socal skateshop scraper
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import cv2

driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver')
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    base_url = 'https://socalskateshop.com/New-Skateboard-Decks.html?&Per_Page=48&Sort_By=name_asc&deckStyle=Standard+Popsicle&CatListingOffset='
    offset = 0 # add 48 to go to next page
    driver.get(base_url + str(offset))

    i = 0
    images_found = True
    while images_found:
        images_found = False
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        for element1 in soup1.find_all('a', class_='u-block x-product-list__link'):
            next_url = element1.get('href')
            driver.get(next_url)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            img_element = soup2.find('img', id='closeup_image', class_='u-hide-visually')
            if img_element is not None:
                img_url = 'https://socalskateshop.com/mm5/' + str(img_element.get('src'))
                images_found = True
                
                # download img; resize to 512x512
                urlretrieve(img_url, f'/tmp/scs_{i}.jpg')
                img = cv2.imread(f'/tmp/scs_{i}.jpg')
                resized_img = cv2.resize(img, (512, 512))
                cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/scs_decks/scs_{i}.png', resized_img)
                i += 1
        offset += 48
        driver.get(base_url + str(offset))

finally:
    driver.quit()