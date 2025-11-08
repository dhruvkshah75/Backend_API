from fastapi import FastAPI, Response, status, HTTPException
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    # post.model_dump()  # post.dict() the dict has been depricated 
    my_posts.append(post_dict)  
    return {
        "data" : post_dict
    }



def find_id(post_id: int):
    for p in my_posts:
        if p['id'] == post_id:
            return p
    return None


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    print(f"The post you are searching has {id}")
    post = find_id(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    return {
        "post detail": post
    }


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

# now deleting a post (CRUD operation)
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found") 
    my_posts.pop(index)  
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_posts(id: int, post_data: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found")
    post_dict = post_data.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {
        "data": post_dict
    }