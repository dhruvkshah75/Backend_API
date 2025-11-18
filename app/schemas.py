from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional


# schema for the user creation
class UserCreate(BaseModel):
    email: EmailStr
    username_id: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username_id: str
    created_at: datetime

    class Config:
        from_attributes = True



# schema for the user login information
class UserLogin(BaseModel):
    identifier: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[int] = None


# The schema of the post data (user input)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

# model of the response that we send to the user
# this class extends PostBase so it has all the feilds of PostBase
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse # returns the user details 

    class Config:
        from_attributes = True



