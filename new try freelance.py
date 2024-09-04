import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--allow-insecure-localhost')

with webdriver.Chrome(options=options) as browser:
    time.sleep(1)
    links = []
    Volumes = []
    Market_caps = []
    names = []
    websites = []
    telegramms = []
    url = 'https://coinmarketcap.com/?page={i}' #You will need to manually set page numbers for place i
    print(f'Navigating to: {url}')
    browser.get(url)
    time.sleep(1)

    page_count = 1

    while True:
        elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))
        )
        item_count = 0
        

        for elem in elements: 
            
            item_count += 1
            print(item_count)
            link = elem.find_element(By.XPATH, ".//a[contains(@href, '/currencies/')]").get_attribute('href')
            links.append(link)
            browser.execute_script(f"window.open('{link}', '_blank');")
            browser.switch_to.window(browser.window_handles[-1])
            
            # Сбор данных
            try:
                time.sleep(1)
                Market_cap = browser.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd').text
                Market_cap_value = Market_cap.split()[-1]
                Market_cap_num = int(Market_cap_value.replace('$', '').replace(',', ''))
                Market_caps.append(Market_cap_num)
            except:
                Market_caps.append('-')

            try:
               time.sleep(1)
               Volume = browser.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').text
               Volume_value = Volume.split()[-1]
               Volume_num = int(Volume_value.replace('$', '').replace(',', ''))
               Volumes.append(Volume_num)
            except:
                Volumes.append('-')
            
            try:
                time.sleep(1)
                name = browser.find_element(By.XPATH, '//span[@data-role="coin-name"]').text
                names.append(name)
                print(name)
            except:
                names.append('-')

            try:
                time.sleep(1)
                website = browser.find_element(By.XPATH, '//*[@data-test="tag-website-links"]').find_element(By.TAG_NAME, 'a').get_attribute('href')
                websites.append(website)
                print(website)
            except:
                websites.append('-')    

            try:
                time.sleep(1)
                telegramm = browser.find_element(By.XPATH, '//*[@data-test="tag-telegram-links"]').find_element(By.TAG_NAME, 'a').get_attribute('href')
                telegramms.append(telegramm)
                print(telegramm)
            except:
                telegramms.append('-')

            time.sleep(0.2)

            # checking if the window exists before closing?
            try:
                browser.close()
            except NoSuchWindowException:
                print("Window already closed.")
            
            # return on base window
            browser.switch_to.window(browser.window_handles[0])
            
        if len(names) == 100:
            break    
    
    


    with open('ksfreelance.csv', 'a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Название', 'Ссылка на страницу', 'Ссылка на сайт', 'Ссылка на телеграмм', 'Сумма капитализации', 'Объем торгов'])
        for i in range(len(names)):
            row = [names[i], links[i], websites[i], telegramms[i], Market_caps[i], Volumes[i]]
            writer.writerow(row)

print("Data scraping complete. Check the 'ksfreelance.csv' file.")
print(url)