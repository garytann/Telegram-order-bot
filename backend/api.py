from fastapi import APIRouter
from endpoints import accounts, orders, menu

api_router = APIRouter()

api_router.include_router(accounts.router, tags=["Accounts"], prefix="/accounts")
api_router.include_router(orders.router, tags=["Orders"], prefix="/orders")
api_router.include_router(menu.router, tags=["Menu"], prefix="/menu")
