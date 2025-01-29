from app.models.pessoa import PessoaBase, Coordenador, Estagiario
from bson import ObjectId
from typing import Optional

class PessoaRepository:
    def __init__(self, db):
        self.db = db["people_db"]

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
    
    async def delete_pessoa(self, pessoa_id: str):
        result = await self.db.pessoas.delete_one(
            { "_id": ObjectId(pessoa_id) }
        )
        return result.deleted_count
    
class CoordenadorRepository:
    def __init__(self, db):
        self.db = db["people_db"]

    async def create_coordenador(self, coordenador: Coordenador):
        result = await self.db.coordenadores.insert_one(coordenador.model_dump())
        return str(result.inserted_id)
    
    async def get_coordenadores(self, filtros: Optional[dict] = None):
        coordenadores = []
        async for coordenador in self.db.coordenadores.find(filtros):
            coordenador["_id"] = str(coordenador["_id"])
            coordenadores.append(coordenador)
        return coordenadores
    
    async def update_coordenador(self, coordenador_id: str, coordenador: Coordenador):
        result = await self.db.coordenadores.update_one(
            { "_id": ObjectId(coordenador_id) }, { "$set": coordenador.model_dump() }
        )
        return result.modified_count
    
    async def delete_coordenador(self, coordenador_id: str):
        result = await self.db.coordenadores.delete_one(
            { "_id": ObjectId(coordenador_id) }
        )
        return result.deleted_count