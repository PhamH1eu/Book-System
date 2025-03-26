from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.AuthorModel import Author, AuthorPublic

class BookBase(SQLModel):
    name: str = Field(index=True)
    author_id: int = Field(foreign_key="author.id")


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: "Author" = Relationship(back_populates="books")


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    name: Optional[str] = None
    author_id: Optional[int] = None


class BookPublic(BookBase):
    id: int
    author: AuthorPublic
