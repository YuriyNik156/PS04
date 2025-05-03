from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org")

assert "Википедия" in browser.title
time.sleep(5)
search_box = browser.find_element(By.NAME, "search")
search_box.send_keys("Солнечная система")
search_box.send_keys(Keys.RETURN)
time.sleep(5)
a = browser.find_element(By.LINK_TEXT, "Солнечная система")
a.click()

input("Нажмите Enter, чтобы завершить скрипт")