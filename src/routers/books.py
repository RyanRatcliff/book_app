from typing import Optional

from starlette import status
from fastapi import APIRouter, HTTPException

from src.models.Book import Book
from src.models.BookRequest import BookRequest

router = APIRouter(
    prefix="/books", tags=["books"], responses={404: {"description": "Not found"}}
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(author: Optional[str] = None):
    return Book.all(author)


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: str):
    book = Book.get_by_id(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Book.create(new_book)
    return new_book


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_id: str, book_request: BookRequest):
    book = Book.get_by_id(book_id)
    if book:
        book = Book.update(Book(**book_request.model_dump()))
        if book:
            return book_request
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    Book.delete(book_id)
