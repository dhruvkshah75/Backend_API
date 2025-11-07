from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# this is called path operation 
@app.get("/")
async def root():
    return {
        "message": "welcome to my api!"
    }


@app.get("/posts")
def get_posts():
    return {
        "data": "This is your post"
    }

# class post extends the BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None   # a completely optional feild 

@app.post("/create_posts")
def create_posts(data: Post):
    print(data)   
    print(data.title)
    return {
        "new_post": f"title: {data.title}, content: {data.content}"
    }