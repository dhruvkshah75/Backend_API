from .. import schemas, utils, models, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import or_
from typing import List

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

# USER crud operations
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_credentials: schemas.UserCreate, db: Session=Depends(get_db)):
    """
    Check if the user already exists by checking the database or else throw a message with 
    Email already registered
    """
    existing_user = db.query(models.User).filter(
        or_(
            models.User.email == user_credentials.email,
            models.User.username_id == user_credentials.username_id
        )
    ).first()
    
    if existing_user:
        # Check which field already exists for a better error message
        if existing_user.email == user_credentials.email:
            detail = "Email already registered"
        else:
            detail = "Username already registered"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)
    
    # hash the password 
    hashed_password = utils.hash(user_credentials.password)
    user_credentials.password = hashed_password
    
    # Create the new user from the input credentials
    new_user = models.User(**user_credentials.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session=Depends(get_db)):
    user_search_query = db.query(models.User).filter(models.User.id == id)

    if user_search_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with id: {id} not found")
    
    user_data = user_search_query.first()
    return user_data



@router.get("/{id}/posts", response_model=List[schemas.PostResponse])
def get_user_posts(id: int, db: Session=Depends(get_db),
                   current_user: dict = Depends(oauth2.get_current_user)):
    """
    We go the /users/id/posts to get all the posts posted by a particular account. 
    First we check if the user id is valid or not and then return the feilds to the user.
    This operation requires the user to be logged in into his account 
    """

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            details="Account with id: {id} not found.")
    else:
        posts_by_user = db.query(models.Post).filter(models.Post.owner_id == id).all()

        return posts_by_user

