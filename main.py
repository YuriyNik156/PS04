from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

service = Service(r"C:\Users\Юрий\Desktop\Google Chrome\chromedriver.exe")
browser = webdriver.Chrome()
browser.get("https://ru.m.wikipedia.org/")
time.sleep(10)
browser.quit()

