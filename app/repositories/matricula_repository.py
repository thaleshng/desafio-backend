from motor.motor_asyncio import AsyncIOMotorDatabase

class MatriculaRepository:
    def __init__(self, db: AsyncIOMotorDatabase, counter_collection: str):
        self.db = db[counter_collection]
    
    async def get_next_matricula(self):
        counter = await self.db.find_one_and_update(
            {"_id": "counter"},
            {"$inc": {"counter": 1}},
            upsert=True,
            return_document=True
        )
        return counter['counter'] 
    
    async def get_matricula_formatada(self, prefix: str) -> str:
        next_number = await self.get_next_matricula()
        matricula = f"{prefix}{next_number:05d}"
        return matricula