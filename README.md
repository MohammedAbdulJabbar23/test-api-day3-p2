# test-api-day3-p2

Blog System
A Blog system with full functionalities of Login/Register, Post,and Comment using FastAPI.



Dependencies:
Package            Version
------------------ --------
aiosqlite          0.17.0
annotated-types    0.6.0
certifi            2024.2.2
fastapi            0.110.0
jose               1.0.0
packaging          23.2
passlib            1.7.4
pip                23.0.1
python-dotenv      1.0.1
python-jose        3.3.0
python-multipart   0.0.9
pytz               2024.1
requests           2.31.0
starlette          0.36.3
tortoise-orm       0.20.0
urllib3            2.2.1
uvicorn            0.27.1




How to use this project:

Linux: python3 -m venv env

source env/bin/activate

pip install [the dependencies mentioned]

uvicorn main:app --reload


    POST /comments - Create a new comment.
        Headers: Authorization: Bearer <token>
        Request Body:

        json

{
    "text": "Your comment text here",
    "postId": 123
}

Response Body:

json

    {
        "id": 1,
        "text": "Your comment text here",
        "postId": 123
    }

POST /register - Register a new user.

    Request Body:

    json

    {
        "username": "moomomo",
        "password": "New comment"
    }

POST /login - Log in an existing user and receive an access token.

    Request Body:

    json

{
    "username": "moomomo",
    "password": "New comment"
}

Response Body:

json

    {
        "access_token": "token",
        "token_type": "token type name"
    }

POST /posts - Create a new post.

    Headers: Authorization: Bearer <token>
    Request Body:

    json

{
    "title": "test post",
    "content": "post testing testing post"
}

Response Body:

json

    {
        "content": "post testing testing post",
        "title": "test post",
        "author_id": 2,
        "id": 1
    }

GET /user/posts-with-comments - Retrieve posts with associated comments for the current user.

POST /posts-with-comments/{user_id} - Retrieve posts with associated comments for a specific user.
