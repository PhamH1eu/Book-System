from typing import List

from app.configs.Database import get_session
from fastapi import Depends
from app.models.AuthorModel import Author
from sqlmodel import Session, select

class AuthorRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_session)) -> None:
        self.db = db

    def list(self) -> List[Author]:
        return self.db.exec(select(Author)).all()

    def get(self, id: int) -> Author:
        return self.db.get(Author, id)

    def create(self, author: Author) -> Author:
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def update(self, author_db: Author) -> Author:
        self.db.add(author_db)
        self.db.commit()
        self.db.refresh(author_db)
        return author_db

    def delete(self, author: Author) -> None:
        self.db.delete(author)
        self.db.commit()
