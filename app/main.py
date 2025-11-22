from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, comment, likes

app = FastAPI()

origins = ["*"]

app .add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comment.router)
app.include_router(likes.router)

# In main.py
from .config import settings
print(f"DEBUG: Current Database URL is: {settings.database_url}")

@app.get("/")
def root():
    return {
        "message": "welcome to my API!"
    }





