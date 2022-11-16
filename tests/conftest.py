"""

Testing database utils.

"""


import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.app import app
from server.config import settings
from server.database import get_db
from server.models import Base
from server.oauth2 import create_access_token
from server import models


SQLALCHEMY_DATABASE_URI = f'postgresql://' \
                          f'{settings.DATABASE_USERNAME}' \
                          f':{settings.DATABASE_PASSWORD}' \
                          f'@{settings.DATABASE_HOSTNAME}' \
                          f':{settings.DATABASE_PORT}' \
                          f'/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def mock_user(client):
    user_data = {
        "email": "ainur@test.com",
        "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def mock_user2(client):
    user_data = {
        "email": "ainur2@test.com",
        "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def access_token(mock_user):
    return create_access_token({"user_id": mock_user['id']})


@pytest.fixture
def authorized_client(client, access_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client


@pytest.fixture
def mock_posts(mock_user, mock_user2, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": mock_user["id"]
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": mock_user["id"]
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": mock_user2["id"]
        },
    ]

    session.add_all([models.Post(**x) for x in posts_data])
    session.commit()

    return session.query(models.Post).all()
