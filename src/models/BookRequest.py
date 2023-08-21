import uuid
from typing import Optional

from pydantic import BaseModel, Field


def default_uuid4():
    return str(uuid.uuid4())


class BookRequest(BaseModel):
    id: Optional[str] = Field(default_factory=default_uuid4)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "4246970c-1c19-4ee9-a280-5717b6929661",
                "title": "A new book",
                "author": "codingwithroby",
                "rating": 5,
            }
        }
