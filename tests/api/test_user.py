import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="Harry",
        last_name="Potter",
        email="harry@hogwarts.com",
        password="passtest",
    )

    response = client.post("/api/register/", payload)

    data = response.data

    pass
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post(
        "/api/login/", dict(email="harry@hogwarts.com", password="passtest")
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client):
    response = client.post(
        "/api/login/", dict(email="harry@hogwarts.com", password="passtest")
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_me(auth_client):
    response = auth_client.get("/api/me/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(auth_client):
    response = auth_client.post("/api/logout/")

    assert response.status_code == 200
    assert response.data["message"] == "so long farewell"
