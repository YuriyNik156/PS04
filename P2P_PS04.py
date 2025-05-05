from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def search_wikipedia(query):
    driver = webdriver.Chrome()  # Убедитесь, что у вас установлен ChromeDriver
    driver.get("https://ru.wikipedia.org/")

    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)  # Ждем загрузки страницы
    return driver


def print_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}:")
        print(paragraph.text)
        print()


def get_related_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    related_links = [link.get_attribute('href') for link in links if '/wiki/' in link.get_attribute('href')]
    return related_links[:10]  # Возвращаем только первые 10 ссылок для простоты


def main():
    query = input("Введите запрос для поиска на Википедии: ")
    driver = search_wikipedia(query)

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == '1':
            print_paragraphs(driver)

        elif choice == '2':
            related_links = get_related_links(driver)
            if not related_links:
                print("Нет связанных страниц.")
                continue

            print("Связанные страницы:")
            for i, link in enumerate(related_links):
                print(f"{i + 1}. {link}")

            page_choice = int(input("Введите номер страницы для перехода: ")) - 1
            if 0 <= page_choice < len(related_links):
                driver.get(related_links[page_choice])
                time.sleep(2)
            else:
                print("Неверный ввод.")

        elif choice == '3':
            print("Выход из программы.")
            driver.quit()
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите корректный номер действия.")

if __name__ == "__main__":
     main()