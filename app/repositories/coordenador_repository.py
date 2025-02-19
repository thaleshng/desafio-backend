from app.models import Coordenador
from bson import ObjectId
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

class CoordenadorRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db["coordenadores"]
        from app.repositories import MatriculaRepository
        self.matricula_repository = MatriculaRepository(db, "coordenador_counter")

    async def create_coordenador(self, coordenador: Coordenador):
        coordenador.matricula = await self.matricula_repository.get_matricula_formatada("COO")

        result = await self.db.coordenadores.insert_one(coordenador.model_dump())
        return str(result.inserted_id)
    
    async def get_coordenadores(self, filtros: Optional[dict] = None):
        coordenadores = []
        async for coordenador in self.db.coordenadores.find(filtros):
            coordenador["_id"] = str(coordenador["_id"])
            coordenadores.append(coordenador)
        return coordenadores
    
    async def update_coordenador(self, coordenador_id: str, coordenador: dict): 
        result = await self.db.coordenadores.update_one(
            { "_id": ObjectId(coordenador_id) }, 
            { "$set": coordenador } 
        )
        return result.modified_count

    async def update_coordenador_by_cpf(self, old_cpf: str, new_cpf: str):
        result = await self.db.coordenadores.update_many(
            {"cpf": old_cpf},
            {"$set": {"cpf": new_cpf}}
        )
        return result.modified_count
    
    async def update_coordenador_fields_by_cpf(self, cpf: str, update_data: dict):
        result = await self.db.coordenadores.update_many(
            {"cpf": cpf},
            {"$set": update_data}
        )
        return result.modified_count
    
    async def delete_coordenador(self, coordenador_id: str):
        result = await self.db.coordenadores.delete_one(
            { "_id": ObjectId(coordenador_id) }
        )
        return result.deleted_count
    
    async def delete_coordenador_by_cpf(self, cpf: str):
        result = await self.db.coordenadores.delete_many({"cpf": cpf})
        return result.deleted_count