import pytest
from rest_framework.test import APIClient
from src.apps.user.services import UserDataClass


@pytest.fixture
def user():
    user_dc = UserDataClass(
        first_name="Harry",
        last_name="Potter",
        email="harry@hogwarts.com",
        password="passtest",
    )

    user = UserDataClass.create_user(user_dc=user_dc)

    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    client.post("/api/login/", dict(email=user.email, password="passtest"))
    return client
