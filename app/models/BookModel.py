from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
import AuthorModel

class Book(SQLModel, table=True):
    id = Optional[int] = Field(default=None, primary_key=True)
    name = str = Field(index=True)
    author_id = int = Field(foreign_key="author.id")
    author: AuthorModel = Relationship(back_populates="books")
