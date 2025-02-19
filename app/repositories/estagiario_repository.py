from app.models import Estagiario
from bson import ObjectId
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

class EstagiarioRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db["estagiarios"]
        from app.repositories import MatriculaRepository
        self.matricula_repository = MatriculaRepository(db, "estagiario_counter")

    async def create_estagiario(self, estagiario: Estagiario):
        estagiario.matricula = await self.matricula_repository.get_matricula_formatada("EST")

        result = await self.db.estagiarios.insert_one(estagiario.model_dump())
        return str(result.inserted_id)

    async def get_estagiarios(self, filtros: Optional[dict] = None):
        estagiarios = []
        async for estagiario in self.db.estagiarios.find(filtros):
            estagiario["_id"] = str(estagiario["_id"])
            estagiarios.append(estagiario)
        return estagiarios
    
    async def update_estagiario(self, estagiario_id: str, estagiario: dict): 
        result = await self.db.estagiarios.update_one(
            { "_id": ObjectId(estagiario_id) }, 
            { "$set": estagiario } 
        )
        return result.modified_count

    async def update_estagiario_by_cpf(self, old_cpf: str, new_cpf: str):
        result = await self.db.estagiarios.update_many(
            {"cpf": old_cpf},
            {"$set": {"cpf": new_cpf}}
        )
        return result.modified_count
    
    async def update_estagiario_fields_by_cpf(self, cpf: str, update_data: dict):
        result = await self.db.estagiarios.update_many(
            {"cpf": cpf},
            {"$set": update_data}
        )
        return result.modified_count
    
    async def delete_estagiario(self, estagiario_id: str):
        result = await self.db.estagiarios.delete_one(
            { "_id": ObjectId(estagiario_id) }
        )
        return result.deleted_count
    
    async def delete_estagiario_by_cpf(self, cpf: str):
        result = await self.db.estagiarios.delete_many({"cpf": cpf})
        return result.deleted_count

