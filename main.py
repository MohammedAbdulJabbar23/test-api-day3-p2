from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

from routes import auth, post, user, comment
from utils import auth as auth_utils

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Register routes
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)

# Initialize Tortoise ORM
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models.post','models.user','models.comment']},
    generate_schemas=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
