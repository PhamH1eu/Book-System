from fastapi import APIRouter

from app.schemas.BookSchema import BookSchema, BookPostSchema

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=BookSchema)
async def get_all_books() -> BookSchema:
    return BookSchema(book_id=123, title="The Great Gatsby", author="F. Scott Fitzgerald")

@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int) -> BookSchema:
    return BookSchema(book_id=book_id, title="The Great Gatsby", author="F. Scott Fitzgerald")

@router.post("/", response_model=BookSchema)
async def create_book(book: BookPostSchema) -> BookSchema:
    return book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookSchema) -> BookSchema:
    return book

@router.delete("/{book_id}") 
async def delete_book(book_id: int):
    return {"message": f"Book {book_id} has been deleted."}

@router.get("/search", response_model=BookSchema)
async def search_books(query: str) -> BookSchema:
    return BookSchema(book_id=123, title="The Great Gatsby", author="F. Scott Fitzgerald")

