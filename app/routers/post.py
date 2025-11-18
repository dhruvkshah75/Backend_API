from .. import schemas, models, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db), 
              current_user: dict = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).all()
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db), 
                 current_user: dict = Depends(oauth2.get_current_user)):
    """ 
    The user needs to be logged in to his account to have access to post.
    So we create a dependency with the oauth2 get_current_user which will raise credentials exception 
    if the user is not logged in or the time of the token has expired 
    We also have to include the owner_id into to the post before adding it to the user 
    """
    # '**' unpacks that dictionary into arguments.
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session=Depends(get_db),
              current_user: dict = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db),
                current_user: dict = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found") 
    else:
        if post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not Authorized to perform requested action")

        post_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.PostResponse)
def update_posts(id: int, post: schemas.PostBase, db: Session=Depends(get_db),
                 current_user: dict = Depends(oauth2.get_current_user)):
    """
    Only the user who is logged in can have access to updating his post 
    We get this from the dependency to get the current_user which verifies that the token is valid or not.
    """

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found")
    else:
        if post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not Authorized to perform requested action")
        
        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        modified_post = post_query.first()
    return modified_post 
