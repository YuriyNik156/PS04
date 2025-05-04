# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# 3.1. листать параграфы текущей статьи;
# 3.2. перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# 3.3. выйти из программы.

# Импортирование библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from delenium.webdriver.common.keys import Keys
import time

# Создание объекта браузера и стартовой страницы
browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")

# Поиск статьи на Википедии
def search_page(query):
    search_box = browser.find_element(By.NAME, "search") # Поле ввода поиска в Википедии
    search_box.clear() # Очистка поля ввода, если что-то прописано
    search_box.send_keys(query) # Ввод в поле строки через аргумент query
    search_box.send_keys(Keys.RETURN) # Отправка запроса в Википедию
    time.sleep(2) # Задержка для загрузки страницы

def get_paragraphs():
    area = browser.find_element(By.ID, "mw-content-text") # Нахождение основной области содержания статьи на странице
    blocks = area.find_elements(By.TAG_NAME, "p") # Выбор всех элементов с тегом <p> из области area
    texts = [] # Список для добавления текста
    for block in blocks: # Перебор абзацев, удаление пустых строк и добавление их в список text
        text = block.text.strip()
        if text:
            texts.append(text)
    return texts

def get_internal_links():
    content_div = browser.find_element(By.ID, "mw-content-text") # Поиск статьи по Id
    links = content_div.find_elements(By.TAG_NAME, "a") # Поиск ссылок по тегу <a>
    result = {} # Словарь для добавления внутренних ссылок
    for link in links: # Перебор все тегов <a>
        href = link.get_attribute("href") # Ссылка
        title = link.get_attribute("title") # Название статьи
        if href and "/wiki/" in href and ":" not in href: # Отбор ссылок только на статьи в Википедии
            result[title] = href
    return result # Возврат значений в виде словаря {Название статьи : ссылка}

