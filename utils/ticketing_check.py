from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
# webdriver, Service, ChromeDriverManager 를 이용한 driver 객체 생성
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20230106')
# print(driver.find_element(by=By.XPATH, value='//*[@id="slider"]/div[1]').text)

print("===")
print(driver.find_element(By.CSS_SELECTOR , 'body'))
print(driver.find_element(By.CSS_SELECTOR , '#ifrm_movie_time_table'))
element = driver.find_element(By.CSS_SELECTOR , '#ifrm_movie_time_table')
driver.switch_to.frame(element)
print(driver.find_element(By.CSS_SELECTOR , 'body > div > div.sect-showtimes > ul > li:nth-child(1) > div > div.info-movie > a > strong'))

# print(driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR , "body > div")))
# print(driver.find_element(By.CSS_SELECTOR , "body").id)
# print(driver.find_element(By.CSS_SELECTOR , "body").location)
# print(driver.find_element(By.CSS_SELECTOR , "body").parent)
# print(driver.find_element(By.CSS_SELECTOR , "body").shadow_root)
# print(driver.find_element(By.CSS_SELECTOR , "body").tag_name)
print("===")
while (True):
    pass
driver.close()

