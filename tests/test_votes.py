import pytest

from server import models


@pytest.fixture
def mock_vote(mock_posts, session, mock_user):
    new_vote = models.Vote(post_id=mock_posts[2].id, user_id=mock_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, mock_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": mock_posts[2].id, "direction": True}
    )
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, mock_posts, mock_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": mock_posts[2].id, "direction": True}
    )
    assert res.status_code == 409


def test_delete_vote(authorized_client, mock_posts, mock_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": mock_posts[2].id, "direction": False}
    )
    assert res.status_code == 201
