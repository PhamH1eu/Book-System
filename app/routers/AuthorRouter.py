from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.models.AuthorModel import AuthorCreate, AuthorPublic, AuthorUpdate
from app.services.AuthorService import AuthorService

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=List[AuthorPublic])
def list_authors(authorService: Annotated[AuthorService, Depends()]):
    authors_response = authorService.list()
    return authors_response


@router.get("/{person_id}", response_model=AuthorPublic)
def get_author(person_id: int, authorService: Annotated[AuthorService, Depends()]):
    author_response = authorService.get(person_id)
    return author_response


@router.post("/", response_model=AuthorPublic)
def create_author(author_new: AuthorCreate, authorService: Annotated[AuthorService, Depends()]):
    response = authorService.create(author_new)
    return response


@router.put("/{person_id}", response_model=AuthorPublic)
def update_author(
    person_id: int, author: AuthorUpdate, authorService: Annotated[AuthorService, Depends()]
):
    update_response = authorService.update(person_id, author)
    return update_response


@router.delete("/{person_id}")
def delete_author(person_id: int, authorService: Annotated[AuthorService, Depends()]):
    authorService.delete(person_id)
    return {"message": f"Author {person_id} has been deleted."}
