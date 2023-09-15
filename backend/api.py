from fastapi import APIRouter
from backend.endpoints import accounts, orders, menu

api_router = APIRouter()

api_router.include_router(accounts.router, tags=["Accounts"])
