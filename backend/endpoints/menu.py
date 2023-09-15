import uvicorn

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

router = APIRouter()

@router.get("/menutest")
async def test():
    return {"test": "test"}