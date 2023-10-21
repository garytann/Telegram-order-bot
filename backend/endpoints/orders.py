import uvicorn

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

# from backend.models.orders import Orders
from models.orders import Orders

router = APIRouter()

@router.get("/ordertest")
async def test():
    return {"test": "test"}

# create new order
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

# list all orders
@router.get("/listorders",
            response_description="List all orders",
            status_code=status.HTTP_200_OK,
            response_model=List[Orders]
            )
async def list_orders(request: Request):
    orders = await request.app.database["Order"].find().to_list(100)
    return orders

# update order
# @router.put("/updateorder/{id}",
#             response_description="Update an order",
#             status_code=status.HTTP_200_OK,
#             response_model=Orders
#             )
# async def update_order(request: Request, id: str, order: Orders = Body(...)):
#     order = {k: v for k, v in order.model_dump().items() if v is not None}
#     if len(order) >= 1:
#         update_result = await request.app.database["Order"].update_one({"_id": id}, {"$set": order})
#         if update_result.modified_count == 1:
#             if (
#                 updated_order := await request.app.database["Order"].find_one({"_id": id})
#             ) is not None:
#                 return updated_order

#     if (existing_order := await request.app.database["Order"].find_one({"_id": id})) is not None:
#         return existing_order

#     raise HTTPException(status_code=404, detail=f"Order {id} not found")

