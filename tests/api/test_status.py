import pytest
from src.apps.status.models import Status


@pytest.mark.django_db
def test_create_status(auth_client, user):
    payload = dict(content="this is a really cool test")
    response = auth_client.post("/api/status/", payload)

    data = response.data

    status_from_db = Status.objects.all().first()

    assert data["content"] == status_from_db.content
    assert data["id"] == status_from_db.id
    assert data["user"]["id"] == user.id


@pytest.mark.django_db
def test_get_user_status(auth_client, user):
    Status.objects.create(user_id=user.id, content="another test status")
    Status.objects.create(user_id=user.id, content="I am a wizard")

    response = auth_client.get("/api/status/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_user_status_detail(auth_client, user):
    status = Status.objects.create(user_id=user.id, content="another test status")
    response = auth_client.get(f"/api/status/{status.id}")
    assert response.status_code == 200
    data = response.data
    assert data["id"] == status.id
    assert data["content"] == status.content


@pytest.mark.django_db
def test_get_user_status_detail_404(auth_client):
    response = auth_client.get("/api/status/0")
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_user_status(auth_client, user):
    status = Status.objects.create(user_id=user.id, content="another test status")
    payload = dict(content="I just updated my status...")

    response = auth_client.put(f"/api/status/{status.id}", payload)

    status.refresh_from_db()
    data = response.data

    assert data["id"] == status.id
    assert status.content == payload["content"]


@pytest.mark.django_db
def test_delete_user_status(auth_client, user):
    status = Status.objects.create(user_id=user.id, content="another test status")
    response = auth_client.delete(f"/api/status/{status.id}")

    assert response.status_code == 204

    with pytest.raises(Status.DoesNotExist):
        status.refresh_from_db()
