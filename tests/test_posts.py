import pytest

from server import schemas


def test_get_all_posts(authorized_client, mock_posts):
    res = authorized_client.get("/posts/")
    posts = [schemas.PostOut(**x) for x in res.json()]

    assert res.status_code == 200
    assert len(posts) == len(mock_posts)


def test_unauthorized_user_get_all_posts(client, mock_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, mock_posts):
    res = client.get(f"/posts/{mock_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, mock_posts):
    res = authorized_client.get("/posts/999999999999")
    assert res.status_code == 404


def test_get_one_post_(authorized_client, mock_posts):
    res = authorized_client.get(f"/posts/{mock_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == mock_posts[0].id
    assert post.Post.content == mock_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("1st title", "1st content", True),
    ("2nd title", "2nd content", True),
    ("3rd title", "3rd content", True),
])
def test_create_post(authorized_client, mock_user, mock_posts, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title, "content": content, "published": published,
    })

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == mock_user['id']


def test_create_post_default_published_true(authorized_client, mock_user):
    res = authorized_client.post("/posts/", json={
        "title": "some title", "content": "some content",
    })

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "some title"
    assert created_post.content == "some content"
    assert created_post.published == True
    assert created_post.owner_id == mock_user['id']


def test_unauthorized_user_create_post(client, mock_user, mock_posts):
    res = client.post("/posts/", json={
        "title": "some title", "content": "some content",
    })
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, mock_user, mock_posts):
    res = client.delete(f"/posts/{mock_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, mock_user, mock_posts):
    res = authorized_client.delete(f"/posts/{mock_posts[0].id}")
    assert res.status_code == 204


def test_delete_other_user_post(authorized_client, mock_user, mock_posts):
    res = authorized_client.delete(
        f"/posts/{mock_posts[2].id}"
    )

    assert res.status_code == 403


def test_update_post(authorized_client, mock_user, mock_posts):
    data = {
        "title": "updated_title",
        "content": "updated_content",
        "id": mock_posts[0].id,
    }

    res = authorized_client.put(
        f"/posts/{mock_posts[0].id}", json=data,
    )

    updated_data = schemas.Post(**res.json())

    assert res.status_code == 201
    assert updated_data.title == data['title']
    assert updated_data.content == data['content']


def test_update_other_user_post(authorized_client, mock_user, mock_posts):
    data = {
        "title": "updated_title",
        "content": "updated_content",
        "id": mock_posts[2].id,
    }

    res = authorized_client.put(
        f"/posts/{mock_posts[2].id}", json=data,
    )

    assert res.status_code == 403
