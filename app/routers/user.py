from .. import schemas, utils, models
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

# USER crud operations
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):

    # hash the password 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.user(**user.model_dump())
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