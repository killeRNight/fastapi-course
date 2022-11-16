import pytest

from server import schemas


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "sigel@test.com",
        "password": "123",
    })
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "sigel@test.com"


def test_login_user(client, mock_user):
    res = client.post("/login", data={
        "username": mock_user["email"],
        "password": mock_user["password"]
    })
    login_res = schemas.Token(**res.json())
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@test.com', '123', 403),
    ('sigel@test.com', 'wrong', 403),
    ('wrong@test.com', 'wrong', 403),
    (None, '123', 422),
    ('sigel@test.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })

    assert res.status_code == status_code
