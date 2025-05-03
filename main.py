from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("https://ru.m.wikipedia.org/")
browser.save_screenshot("dom.png")
time.sleep(5)
browser.get("https://ru.wikipedia.org/wiki/Selenium")
browser.save_screenshot("selenium.png")
time.sleep(3)
browser.refresh()

input("Нажмите Enter, чтобы завершить скрипт")