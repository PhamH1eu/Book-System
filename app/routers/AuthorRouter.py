from fastapi import APIRouter

from app.schemas.AuthorSchema import AuthorSchema, AuthorPostSchema

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/", response_model=AuthorSchema)
async def get_author(person_id: int) -> AuthorSchema:
    return AuthorSchema(person_id=person_id, name="F. Scott Fitzgerald")

@router.post("/", response_model=AuthorSchema)
async def create_author(author: AuthorPostSchema) -> AuthorSchema:
    return author

@router.put("/{person_id}", response_model=AuthorSchema)
async def update_author(person_id: int, author: AuthorSchema) -> AuthorSchema:
    return author

@router.delete("/{person_id}")
async def delete_author(person_id: int):
    return {"message": f"Author {person_id} has been deleted."}