from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(
    "mongodb+srv://thaleshng:3XfHSCW9mQAj2ggp@people-db.ukd26.mongodb.net/?retryWrites=true&w=majority&appName=people-db"
)
    app.mongodb_db = app.mongodb_client["people_db"]
    print("MongoDB Conectado!")

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()
    print("MongoDB Desconectado!")
