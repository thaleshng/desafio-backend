from app.models import PessoaBase
from bson import ObjectId
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

class PessoaRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db["pessoas"]

    async def create_pessoa(self, pessoa: PessoaBase):
        result = await self.db.pessoas.insert_one(pessoa.model_dump())
        return str(result.inserted_id)
    
    async def get_pessoas(self, filtros: Optional[dict] = None):
        pessoas = []
        async for pessoa in self.db.pessoas.find(filtros):
            pessoa["_id"] = str(pessoa["_id"])
            pessoas.append(pessoa)
        return pessoas
    
    async def update_pessoa(self, pessoa_id: str, pessoa: PessoaBase):
        result = await self.db.pessoas.update_one(
            { "_id": ObjectId(pessoa_id) }, { "$set": pessoa.model_dump() }
        )
        return result.modified_count
    
    async def update_pessoa_by_cpf(self, old_cpf: str, new_cpf: str):
        result = await self.db.pessoas.update_one(
            {"cpf": old_cpf},
            {"$set": {"cpf": new_cpf}}
        )
        return result.modified_count
    
    async def delete_pessoa(self, pessoa_id: str):
        result = await self.db.pessoas.delete_one(
            { "_id": ObjectId(pessoa_id) }
        )
        return result.deleted_count
    
    async def delete_pessoa_by_cpf(self, cpf: str):
        result = await self.db.pessoas.delete_one({"cpf": cpf})
        return result.deleted_count