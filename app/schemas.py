from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# schema for response
class Post(PostBase):
    id: int
    created_at: datetime