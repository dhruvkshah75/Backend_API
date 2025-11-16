from pydantic import BaseModel
from datetime import datetime 

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
    
    class Config:
        from_attributes = True