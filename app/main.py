from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# The schema of the post data (user input)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {
        "message": "welcome to my api!"
    }


@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.posts).all()
    return { "posts details": posts }



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session=Depends(get_db)):
    # 'model_dump()' converts the Pydantic model to a dictionary.
    # '**' unpacks that dictionary into arguments.
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"post detail": new_post}



@app.get("/posts/{id}")
def get_posts(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    return {
        "post detail": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found") 
    else:
        post_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_posts(id: int, post: Post, db: Session=Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found")
    else:
        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        modified_post = post_query.first()
    return { "post detail": modified_post }


