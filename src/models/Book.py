from src.models.DynamoBook import DynamoBook
from fastapi.responses import JSONResponse


class Book:
    def __init__(self, id, title, author, rating):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

    def __repr__(self):
        return f"<Book {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
        }

    @staticmethod
    def all(author=None):
        books = (
            DynamoBook.scan(DynamoBook.author == author)
            if author
            else DynamoBook.scan()
        )
        results = []
        for book in books:
            results.append(book.attribute_values)
        return JSONResponse(content=results)

    @staticmethod
    def get_by_id(id) -> dict | None:
        try:
            book = DynamoBook.get(id)
            return book.attribute_values

        except DynamoBook.DoesNotExist:
            return None

    @staticmethod
    def create(book):
        DynamoBook(**book.to_dict()).save()
        return book

    @staticmethod
    def update(updates):
        try:
            book = DynamoBook.get(updates.id)
            book.rating = updates.rating
            book.author = updates.author
            book.title = updates.title
            book.save()
            return book.attribute_values

        except DynamoBook.DoesNotExist:
            return None

    @staticmethod
    def delete(id: str):
        try:
            book = DynamoBook.get(id)
            book.delete()

        except DynamoBook.DoesNotExist:
            return None
