from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# list to store data of each posts
# hardcoded 2 values 
my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]  

# this is called path operation 
@app.get("/")
async def root():
    return {
        "message": "welcome to my api!"
    }


@app.get("/posts")
def get_posts():
    return {
        "data": my_posts
    }

# class post extends the BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None   # a completely optional feild 

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    # post.model_dump()  # post.dict() the dict has been depricated 
    my_posts.append(post_dict)  
    return {
        "data" : post_dict
    }



@app.get("/posts/{id}")
def get_posts(id):
    print(id)
    return {
        "post detail": f"Here is the post with the {id}"
    }
