from pydantic import BaseModel

class AuthorSchema(BaseModel):
    person_id: int
    name: str

class AuthorPostSchema(BaseModel):
    name: str