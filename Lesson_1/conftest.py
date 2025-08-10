import pytest
import yaml
import requests

@pytest.fixture(scope="session")
def config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def login(config):
    response = requests.post(
        config["address"] + "gateway/login",
        data={"username": config["username"], "password": config["password"]}
    )
    response.raise_for_status()
    return response.json()["token"]