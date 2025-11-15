from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connected successfully!")
        break
    
    except Exception as error:
        print(f"Error connecting to the database! Error: {error}")
        time.sleep(3)

@app.get("/test_post")
def test_posts(db: Session = Depends(get_db)):
    return { "status": "success"}


# this is called path operation 
@app.get("/")
async def root():
    return {
        "message": "welcome to my api!"
    }


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall() 
    return { "post detail": posts }



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {"post detail": new_post}



@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    return {
        "post detail": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found") 
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                   (post.title, post.content, post.published, str(id),))
    modified_post = cursor.fetchone()

    if modified_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found")
    
    conn.commit()
    return { "post detail": modified_post }


