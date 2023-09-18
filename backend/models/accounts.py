import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Accounts (BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    userid: str = Field(...)
    name: str = Field(...)
    contact: str = Field(...)
    address: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "userid": "192070187",
                "name": "John Doe",
                "contact": "12345678",
                "address": "hall 11"
            }
        }