from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time


def test_create_post_ui(driver, config):
    wait = WebDriverWait(driver, 20)

    # Открываем страницу логина
    driver.get(config["address"] + "/login")

    # Ждём появления формы логина
    username_input = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//label[.//span[contains(text(), 'Username')]]//input"
    )))
    username_input.send_keys(config["username"])

    password_input = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//label[.//span[contains(text(), 'Password')]]//input"
    )))
    password_input.send_keys(config["password"])

    # Кликаем кнопку входа
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()

    # Ждём перехода на главную страницу
    wait.until(EC.url_to_be(config["address"] + "/"))

    # Нажимаем кнопку создания поста
    create_post_button = wait.until(EC.element_to_be_clickable((By.ID, "create-btn")))
    create_post_button.click()

    # Ждём загрузки страницы создания поста
    wait.until(EC.url_contains("/posts/create"))
    print(f"Текущий URL: {driver.current_url}")
    print("Страница создания поста загружена")

    # Уникальный заголовок поста
    unique_title = f"Тестовый пост {random.randint(1000, 9999)}"
    unique_description = f"Описание {random.randint(1000, 9999)}"
    content_text = "Автотест контент"

    # Вводим Title (по тексту Label → input)
    title_input = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[.//span[text()='Title']]//input"
    )))
    title_input.send_keys(unique_title)

    # Вводим Description (по тексту Label → textarea)
    description_input = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[.//span[text()='Description']]//textarea"
    )))
    description_input.send_keys(unique_description)

    # Вводим Content (по тексту Label → textarea)
    content_input = wait.until(EC.presence_of_element_located((
        By.XPATH, "//label[.//span[text()='Content']]//textarea"
    )))
    content_input.send_keys(content_text)

    # Кликаем кнопку Save (по тексту кнопки)
    save_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[.//span[text()='Save']]"
    )))
    save_button.click()

    # Подождём немного, чтобы страница успела обновиться
    time.sleep(3)

    # Проверяем, что заголовок нового поста появился на странице (ищем по тексту)
    page_source = driver.page_source
    assert unique_title in page_source, f"Заголовок '{unique_title}' не найден на странице"

    print(f"Пост '{unique_title}' успешно создан и отображается на странице.")