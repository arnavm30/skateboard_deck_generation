# tgm skateboards scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import cv2

opts = Options()
opts.add_argument('user-agent=haha') # changing user-agent
driver = webdriver.Chrome('/home/arnav/Workarea/Deck_Designs/chromedriver', chrome_options=opts)
driver.implicitly_wait(30) # wait 30 seconds for element before throwing exception

try:
    base_url = 'https://tgmskateboards.com/skateboards-longboard/skateboards/decks/?sort=featured&page='
    page = 1
    driver.get(base_url + str(page))

    i = 0
    images_found = True
    while images_found:
        images_found = False
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        for element1 in soup1.find_all('figure', class_='card-figure'):
            for element2 in element1.find_all('a', attrs={'href': re.compile(r'^(http|https)://')}):
                next_url = element2.get('href')
                driver.get(next_url)
                soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                img_element = soup2.find('a', attrs={'href': re.compile(r'/1280x1280/')})
                if img_element is not None:
                    img_url = img_element.get('href')
                    images_found = True

                    # if img_url leads to img in form of gif, download the 1 frame
                    if img_url[-7:-4] == 'gif':
                        urlretrieve(img_url, f'/tmp/tgms_{i}.gif')
                        gif = cv2.VideoCapture(f'/tmp/tgms_{i}.gif')
                        ret, frame = gif.read()
                        cv2.imwrite(f'/tmp/tgms_{i}.jpg', frame)
                    else:
                        urlretrieve(img_url, f'/tmp/tgms_{i}.jpg')
                    # resize to 512 x 512
                    img = cv2.imread(f'/tmp/tgms_{i}.jpg')
                    resized_img = cv2.resize(img, (512, 512))
                    cv2.imwrite(f'/home/arnav/Workarea/Deck_Designs/deks/tgms_{i}.png', resized_img)
                    i += 1
        page += 1
        driver.get(base_url + str(page))

finally:
    driver.quit()



'''
    next_page = driver.find_element_by_class_name('bold-blocks-a__link.bold-blocks-a__link--arrow')
    print(next_page)

    while next_page:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product-listing-container"]/div[1]/div[2]/ul/li[9]/a'))).click()
        time.sleep(5)

        next_page.click()
        next_page = driver.find_element_by_xpath(r'//*[@id="product-listing-container"]/div[1]/div[2]/ul/li[9]/a')
        print(next_page)
'''