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
from selenium.webdriver.common.keys import Keys
import time

# Создание объекта браузера и стартовой страницы Википедии
browser = webdriver.Google()
browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")


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
        return

    # Если это страница значений
    if is_disambiguation_page():
        print("Обнаружена страница значений. Пытаемся выбрать первую подходящую статью...")
        links = get_internal_links()
        valid_links = {title: url for title, url in links.items()
                        if title and ":" not in title and title.lower() != query.lower()}
        if valid_links:
            first_title = list(valid_links.keys())[0]
            browser.get(valid_links[first_title])
            time.sleep(2)
        else:
            print("Не удалось найти подходящую статью. Попробуйте другой запрос.")

def is_disambiguation_page():
    try:
        # Проверка, есть ли на странице класс, указывающий на страницу значений
        disambig = browser.find_element(By.CLASS_NAME, "mw-disambig")
        return True
    except:
        return False

# Извлечение параграфов из основной статьи на Википедии
def get_paragraphs():
    area = browser.find_element(By.ID, "mw-content-text") # Нахождение основной области содержания статьи на странице
    blocks = area.find_elements(By.TAG_NAME, "p") # Выбор всех элементов с тегом <p> из области area
    texts = [] # Список для добавления текста
    for block in blocks: # Перебор абзацев, удаление пустых строк и добавление их в список text
        text = block.text.strip()
        if text:
            texts.append(text)
    return texts

# Поиск внутренних ссылок википедии
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

# Предложение пользователю три варианта действий
def choose_action():
    print("\nЧто вы хотите сделать?")
    print("1 - Листать параграфы текущей статьи")
    print("2 - Перейти на связанную статью")
    print("3 - Выйти")
    return input("Введите номер действия: ")

# Вывод параграфов и возможность их перелистывания
def show_paragraphs():
    paragraphs = get_paragraphs() # Получение параграфов текущей статьи
    if not paragraphs: # Если параграф пустой
        print("Параграфы не найдены.")
        return
    for i, p in enumerate(paragraphs): # Перебор и вывод параграфов
        print(f"\n--- Параграф {i+1} ---\n{p}")
        if i < len(paragraphs) - 1: # Перелистывание параграфов клавишей Enter
            cont = input("\nНажмите Enter для следующего параграфа или введите 'q' для выхода: ")
            if cont.lower() == 'q':
                break

# Переход по внутренней ссылке из текущей статьи
def navigate_internal_link():
    links = get_internal_links() # Словарь внутренних ссылок
    if not links: # Если словарь пустой
        print("Внутренние ссылки не найдены.")
        return
    link_titles = list(links.keys())[:10] # Берутся первые 10 ссылок из словаря
    print("\nВыберите статью для перехода:")
    for i, title in enumerate(link_titles): # Отображение 10 ссылок
        print(f"{i+1} - {title}")
    choice = input("Введите номер статьи или 'q' для отмены: ") # Выбор пользователем статьи
    if choice.isdigit() and 1 <= int(choice) <= len(link_titles): # Проверка ввода пользователем числа
        selected = link_titles[int(choice)-1]
        browser.get(links[selected])
        time.sleep(2) # Задержка для загрузки страницы
        main_loop() # Повторный запуск основного цикла

# Основной цикл поиска статей в Википедии
def main_loop():
    while True:
        action = choose_action()
        if action == '1':
            show_paragraphs()
        elif action == '2':
            navigate_internal_link()
        elif action == '3':
            print("Выход из программы.")
            browser.quit()
            break
        else:
            print("Некорректный ввод. Повторите попытку.")

# Основной запуск
user_query = input("Введите поисковый запрос на Википедии: ")
search_page(user_query)
main_loop()