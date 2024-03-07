from fastapi.testclient import TestClient
from main import app
from models.user import User
from models.post import Post

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register",
        json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert "id" in response.json()

# Test user login
def test_login():
    response = client.post(
        "/login",
        data={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    global access_token
    access_token = response.json()["access_token"]

def test_get_user_details():
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"

def test_create_comment():
    user = User(username="test_user")
    user.save()

    # create a test post
    post = Post(title="Test Post", content="Test Content", author=user)
    post.save()

    # send request to create a comment
    response = client.post(
        "/comments/",
        json={"text": "Test Comment", "post_id": post.id},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["text"] == "Test Comment"

# test getting all comments
def test_read_comments():
    response = client.get("/comments/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# test getting a specific comment
def test_read_comment():
    # get the ID of the first comment
    response = client.get("/comments/")
    comment_id = response.json()[0]["id"]

    # send request to get the specific comment
    response = client.get(f"/comments/{comment_id}/")
    assert response.status_code == 200
    assert response.json()["id"] == comment_id

# test updating a comment
def test_update_comment():
    # Get the ID of the first comment
    response = client.get("/comments/")
    comment_id = response.json()[0]["id"]

    # Send request to update the specific comment
    response = client.put(
        f"/comments/{comment_id}/",
        json={"text": "Updated Comment"},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["text"] == "Updated Comment"

# test deleting a comment
def test_delete_comment():
    # get the ID of the first comment
    response = client.get("/comments/")
    comment_id = response.json()[0]["id"]

    # send request to delete the specific comment
    response = client.delete(f"/comments/{comment_id}/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully"
