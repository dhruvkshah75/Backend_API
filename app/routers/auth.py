from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import oauth2, utils, database, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    """
    It is post operation as the user provides in with the email and password
    Checks if the email is present in the database or not and then 
    verifies if the password is correct with the help of utils.py file 
    and creates a jwt token for the user
    """
    # OAuth2PasswordAuthentication has username and password
    user_email_query = db.query(models.User).filter(models.User.email == user_info.username)

    user = user_email_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f'Invalid Credentials')
    else:
        if not utils.verify(user_info.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f'Invalid Credentials')
    # create a token from the oauth2.py with the payload data as user_id
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    
    return {"access_token": access_token, "token_type": "bearer"}
