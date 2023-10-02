import uvicorn

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from backend.models.orders import Orders

router = APIRouter()

@router.get("/ordertest")
async def test():
    return {"test": "test"}

@router.post("/createorders",
             response_description="create a new order",
             status_code=status.HTTP_201_CREATED,
            response_model = Orders
             )
async def create_order(request: Request, order: Orders = Body(...)):
    order = jsonable_encoder(order)
    new_order = await request.app.database["Order"].insert_one(order)
    created_order = await request.app.database["Order"].find_one({"_id": new_order.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)
    return created_order


@router.get("/listorders",
            response_description="List all orders",
            status_code=status.HTTP_200_OK,
            response_model=List[Orders]
            )
async def list_orders(request: Request):
    orders = await request.app.database["Order"].find().to_list(100)
    return orders

