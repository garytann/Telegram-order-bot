import uvicorn

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from backend.models import Accounts

router = APIRouter()

@router.get("/accountstest")
async def test():
    return {"test": "test"}

@router.post("/register", 
            response_description="create a new account", 
            status_code=status.HTTP_201_CREATED, 
            response_model = Accounts)
async def create_account(request: Request, account: Accounts = Body(...)):
    account = jsonable_encoder(account)
    new_account = await request.app.mongodb["Accounts"].insert_one(account)
    created_account = await request.app.mongodb["Accounts"].find_one({"_id": new_account.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_account)
    return created_account



