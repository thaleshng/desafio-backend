import os
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    app.mongodb_db = app.mongodb_client[os.getenv("MONGODB_DB")]
    print("MongoDB Conectado!")

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()
    print("MongoDB Desconectado!")
