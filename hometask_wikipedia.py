# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# 3.1. листать параграфы текущей статьи;
# 3.2. перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# 3.3. выйти из программы.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Создание объекта браузера и стартовой страницы Википедии
browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/Заглавная_страница")

# Проверка: если нас перекинуло на страницу поиска
def search_page(query):
    search_box = browser.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        # Проверим, есть ли основной текст статьи
        browser.find_element(By.ID, "mw-content-text")
    except:
        print("Точная статья не найдена. Попробуйте ввести более конкретный запрос.")
        return False

    # Если это страница значений
    if is_disambiguation_page():
        print("Обнаружена страница значений. Выберите одну из предложенных статей:")
        links = get_internal_links()
        valid_links = {title: url for title, url in links.items() if title and ":" not in title}
        if valid_links:
            for i, (title, url) in enumerate(valid_links.items(), 1):
                print(f"{i}. {title}")
            try:
                choice = int(input("Введите номер статьи: "))
                selected_url = list(valid_links.values())[choice - 1]
                browser.get(selected_url)
                time.sleep(2)
            except (ValueError, IndexError):
                print("Некорректный выбор. Попробуйте снова.")
                return False
        else:
            print("Не удалось найти подходящую статью. Попробуйте другой запрос.")
            return False
    return True

def is_disambiguation_page():
    try:
        browser.find_element(By.CLASS_NAME, "mw-disambig")
        return True
    except:
        return False

# Извлечение параграфов из основной статьи на Википедии
def get_paragraphs():
    area = browser.find_element(By.ID, "mw-content-text")
    blocks = area.find_elements(By.TAG_NAME, "p")
    texts = []
    for block in blocks:
        text = block.text.strip()
        if text:
            texts.append(text)
    return texts

# Поиск внутренних ссылок википедии
def get_internal_links():
    content_div = browser.find_element(By.ID, "mw-content-text")
    links = content_div.find_elements(By.TAG_NAME, "a")
    result = {}
    for link in links:
        href = link.get_attribute("href")
        title = link.get_attribute("title")
        if href and "/wiki/" in href and ":" not in href:
            result[title] = href
    return result

# Предложение пользователю три варианта действий
def choose_action():
    print("\nЧто вы хотите сделать?")
    print("1 - Листать параграфы текущей статьи")
    print("2 - Перейти на связанную статью")
    print("3 - Выйти")
    return input("Введите номер действия: ")

# Основной цикл программы
def main():
    try:
        while True:
            query = input("Введите запрос для поиска на Википедии: ")
            if not search_page(query):
                continue

            while True:
                action = choose_action()
                if action == "1":
                    paragraphs = get_paragraphs()
                    for i, paragraph in enumerate(paragraphs, 1):
                        print(f"{i}. {paragraph}")
                        input("Нажмите Enter для продолжения...")
                elif action == "2":
                    links = get_internal_links()
                    if not links:
                        print("В статье нет связанных ссылок.")
                        continue

                    print("Выберите одну из связанных статей:")
                    valid_links = {title: url for title, url in links.items() if title}
                    for i, (title, url) in enumerate(valid_links.items(), 1):
                        print(f"{i}. {title}")

                    try:
                        choice = int(input("Введите номер статьи: "))
                        selected_url = list(valid_links.values())[choice - 1]
                        browser.get(selected_url)
                        time.sleep(2)
                    except (ValueError, IndexError):
                        print("Некорректный выбор. Попробуйте снова.")
                        continue
                elif action == "3":
                    print("Выход из программы...")
                    browser.quit()
                    return
                else:
                    print("Некорректный выбор. Попробуйте снова.")
    except KeyboardInterrupt:
        print("\nВыход из программы...")
        browser.quit()

if __name__ == "__main__":
    main()