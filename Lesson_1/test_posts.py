import pytest
import requests
import random

class TestPosts:

    @pytest.mark.parametrize("expected_title", [
        "тра тата удалить",
        "Пишу черновик"  # актуальное название поста, которое видно на сервере
    ])
    def test_post_title_exists(self, login, config, expected_title):
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

    def test_create_post_and_check_description(self, login, config):
        headers = {"X-Auth-Token": login}

        unique_description = f"Описание_{random.randint(1000, 9999)}"

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

        # Получаем список своих постов
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