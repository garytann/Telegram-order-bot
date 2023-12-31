import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Accounts (BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    userid: str = Field(...)
    name: str = Field(...)
    contact: str = Field(...)
    address: str = Field(...)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "userid": "192070187",
                "name": "John Doe",
                "contact": "12345678",
                "address": "hall 11"
            }
        }