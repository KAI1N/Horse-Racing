#selenium 3.141.0
from selenium import webdriver
from time import sleep
driver = webdriver.Chrome("C:/Users/khata/OneDrive/デスクトップ/Horse Racing/chromedriver-win32/chromedriver.exe")
driver.get('https://www.google.co.jp')
search_bar=driver.find_element_by_name('q')
search_bar.send_keys('python')
search_bar.submit()
