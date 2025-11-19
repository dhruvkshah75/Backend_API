from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional, Literal


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



class CommentCreate(BaseModel):
    content: str

# What you send back
class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    post_id: int
    owner_id: int
    owner: UserResponse # return the user details 
    parent_post: PostResponse  # return the parent post detail
    
    class Config:
        from_attributes = True


class Like(BaseModel):
    target_id: int # 'target_id' will be the post_id or comment_id
    direction: Literal[0, 1] # 'direction' is 1 for like, 0 for unlike
    target_type: Literal['post', 'comment'] # 'target_type' specifies what is being liked

