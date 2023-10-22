from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Orders (BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    date: datetime = Field(default_factory=datetime.now)
    order: str = Field(...)
    name: str = Field(...)
    address : str = Field(...)
    userid: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "date": "07-04-2023",
                "order": "selection01",
                "name": "John Doe",
                "address": "hall 11",
                "userid": "1234567"                
            }
        }

class OrdersUpdate(BaseModel):
    date: Optional[datetime]
    order: Optional[str]
    name: Optional[str]
    address: Optional[str]
    # userid: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "date": "07-04-2023",
                "order": "selection01",
                "name": "John Doe",
                "address": "hall 11",
                # "userid": "1234567"                
            }
        }