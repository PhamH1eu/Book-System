from typing import List

from fastapi import Depends

from app.models.BookModel import Book, BookCreate, BookUpdate
from app.repositories.BookRepo import BookRepository
from app.services.AuthorService import AuthorService

from app.exceptions import ResourceNotFoundException

class BookService:
    bookRepo: BookRepository
    authorService: AuthorService

    def __init__(
        self,
        bookRepo: BookRepository = Depends(),
        authorService: AuthorService = Depends(),
    ) -> None:
        self.bookRepo = bookRepo
        self.authorService = authorService

    def create(self, book: BookCreate) -> Book:
        if book.author_id:
            if not self.authorService.get(book.author_id):
                raise ResourceNotFoundException(resource="Author", resource_id=book.author_id)
        db_book = Book.model_validate(book)
        return self.bookRepo.create(db_book)

    def list(self) -> List[Book]:
        return self.bookRepo.list()

    def get(self, id: int) -> Book:
        return self.bookRepo.get(id)

    def update(self, id: int, book: BookUpdate) -> Book:
        if book.author_id:
            if not self.authorService.get(book.author_id):
                raise ResourceNotFoundException(resource="Author", resource_id=book.author_id)
        book_db = self.bookRepo.get(id)
        if not book_db:
            raise ResourceNotFoundException(resource="Book", resource_id=id)
        book_data = book.model_dump(exclude_unset=True)
        book_db.sqlmodel_update(book_data)
        print(book_db)
        return self.bookRepo.update(book_db)

    def delete(self, id: int) -> None:
        book = self.bookRepo.get(id)
        if not book:
            raise ResourceNotFoundException(resource="Book", resource_id=id)
        return self.bookRepo.delete(book)
