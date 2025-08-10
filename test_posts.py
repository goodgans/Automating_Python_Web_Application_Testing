import pytest
import requests
import random

@pytest.mark.parametrize("expected_title", [
    "тра тата удалить",
    "GeekTEST Post"
])
def test_post_title_exists(login, config, expected_title):
    headers = {"X-Auth-Token": login}
    response = requests.get(
        config["address"] + "api/posts",
        headers=headers,
        params={"owner": "notMe"}
    )
    response.raise_for_status()
    posts = response.json()["data"]

    titles = [post["title"] for post in posts]
    print(f"Полученные заголовки: {titles}")

    assert expected_title in titles, f"Заголовок '{expected_title}' не найден среди постов"

# ✅ Новый тест — создание поста и проверка по описанию
def test_create_post_and_check_description(login, config):
    headers = {"X-Auth-Token": login}
    
    # Делаем уникальное описание, чтобы проверить потом
    unique_description = f"Описание_{random.randint(1000,9999)}"

    # Данные нового поста
    post_data = {
        "title": "Тестовый заголовок",
        "description": unique_description,
        "content": "Тестовое содержимое"
    }

    # Создание поста
    response = requests.post(
        config["address"] + "api/posts",
        headers=headers,
        data=post_data
    )
    response.raise_for_status()

    # Проверяем, что пост с таким description появился
    get_response = requests.get(
        config["address"] + "api/posts",
        headers=headers,
        params={"owner": "me"}
    )
    get_response.raise_for_status()
    posts = get_response.json()["data"]

    descriptions = [post["description"] for post in posts]
    print(f"Полученные описания: {descriptions}")

    assert unique_description in descriptions, f"Описание '{unique_description}' не найдено среди постов"