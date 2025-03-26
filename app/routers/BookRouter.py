from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.BookModel import BookCreate, BookPublic, BookUpdate
from app.services.AuthorService import AuthorService
from app.services.BookService import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookPublic])
def get_all_books(bookService: BookService = Depends()):
    return bookService.list()


@router.get("/{book_id}", response_model=BookPublic)
def get_book(book_id: int, bookService: BookService = Depends()):
    return bookService.get(book_id)


@router.post("/", response_model=BookPublic)
def create_book(book: BookCreate, bookService: BookService = Depends()):
    return bookService.create(book)


@router.put("/{book_id}", response_model=BookPublic)
def update_book(
    book_id: int,
    book: BookUpdate,
    bookService: BookService = Depends(),
    authorService: AuthorService = Depends(),
):
    if book.author_id:
        if not authorService.get(book.author_id):
            raise HTTPException(status_code=404, detail="Author not found")
    return bookService.update(book_id, book)


@router.delete("/{book_id}")
def delete_book(book_id: int, bookService: BookService = Depends()):
    bookService.delete(book_id)
    return {"message": f"Book {book_id} has been deleted."}


# @router.get("/search", response_model=BookPublic)
# def search_books(query: str):
#     pass
