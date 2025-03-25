from pydantic import BaseModel

class BookSchema(BaseModel):
    book_id: int
    title: str
    author: str

class BookPostSchema(BaseModel):
    title: str
    author_id: int