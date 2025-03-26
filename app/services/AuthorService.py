from typing import List

from fastapi import Depends, HTTPException

from app.models.AuthorModel import Author, AuthorCreate, AuthorUpdate
from app.repositories.AuthorRepo import AuthorRepository


class AuthorService:
    authorRepo: AuthorRepository

    def __init__(self, authorRepo: AuthorRepository = Depends()) -> None:
        self.authorRepo = authorRepo

    def create(self, author: AuthorCreate) -> Author:
        db_author = Author.model_validate(author)
        return self.authorRepo.create(db_author)

    def list(self) -> List[Author]:
        return self.authorRepo.list()

    def get(self, id: int) -> Author:
        return self.authorRepo.get(id)

    def update(self, id: int, author: AuthorUpdate) -> Author:
        author_db = self.authorRepo.get(id)
        if not author_db:
            raise HTTPException(status_code=404, detail="Author not found")
        author_data = author.model_dump(exclude_unset=True)
        author_db.sqlmodel_update(author_data)
        return self.authorRepo.update(author_db)

    def delete(self, id: int) -> None:
        author = self.authorRepo.get(id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return self.authorRepo.delete(author)
