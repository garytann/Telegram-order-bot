
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import cors
from motor.motor_asyncio import AsyncIOMotorClient


from backend.api import api_router

import os
from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv('bot_token')
DB_USER = os.getenv('db_user')
db_password = os.getenv('db_password')

# uri = f"mongodb+srv://{db_user}:{db_password}@atlascluster.x0j1zkf.mongodb.net/?retryWrites=true&w=majority"
URI = os.getenv('ATLAS_URI')

app = FastAPI()

app.include_router(api_router)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    # app.mongodb_client = MongoClient(URI,server_api=ServerApi('1'))
    app.mongodb_client = AsyncIOMotorClient(URI,server_api=ServerApi('1'))
    app.database = app.mongodb_client["AcaiDB"]
    try:
        app.mongodb_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return app.database

# Create a new client and connect to the server
# client = MongoClient(URI, server_api=ServerApi('1'))

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


# def get_database(db: AsyncIOMotorClient = Depends(startup_db_client)):
#     return db

# db = client.AcaiDB

# accounts_collection = db.Accounts
# orders_collection = db.Orders

# accounts_docs = {
#                     "name": "john doe", 
#                     "contact": 12345678, 
#                     "email": "john@gmail.com",
#                     "address": "hall11" 
#                     }

# # Insert a document into the 'users' collection
# try: 
#  result = accounts_collection.insert_one(accounts_docs)

# # return a friendly error if the operation fails
# except pymongo.errors.OperationFailure:
#   print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
#   sys.exit(1)
# else:
    
#   print("insertion success")
#   inserted_count = result.inserted_id
#   print(f"I inserted %x documents.({inserted_count})")

#   print("\n")


# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

