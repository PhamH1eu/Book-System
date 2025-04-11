from typing import List

from fastapi import Depends
from sqlmodel import Session, select, text

from app.configs.Database import get_session
from app.models.BookModel import Book


class BookRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_session)) -> None:
        self.db = db

    def list(self) -> List[Book]:
        return self.db.exec(select(Book)).all()

    def get(self, id: int) -> Book:
        return self.db.get(Book, id)

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, book_db: Book) -> Book:
        self.db.add(book_db)
        self.db.commit()
        self.db.refresh(book_db)
        return book_db

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()

    def search(self, keyword: str):
        query = text("SELECT * FROM book WHERE tsv @@ to_tsquery(:keyword)")
        results = self.db.exec(query, {"keyword": keyword}).all()
        return [Book.model_validate(result) for result in results]
