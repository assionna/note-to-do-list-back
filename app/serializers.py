from pydantic import BaseModel
from typing import List


class CategorySerializer(BaseModel):
    name: str


class NotesSerializer(BaseModel):
    title: str
    body: str
    # category: Category
