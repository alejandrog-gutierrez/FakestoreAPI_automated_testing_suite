import pytest
import requests

@pytest.fixture(scope="session")
def session():
    with requests.Session() as s:
        yield s

@pytest.fixture(scope="session")
def base_url():
    return "https://fakestoreapi.com"

# @pytest.fixture(scope="session")
# def auth_token(session,base_url):
#     auth_token = session.post(f'{base_url}/auth/login',json={"username":"john_doe","password":"pass123"}).json()
#     return auth_token["token"]
#This fixture was originally thought for authenticated cases, but it was never used anyways, since the API does not rely on tokens for the endpoints.
