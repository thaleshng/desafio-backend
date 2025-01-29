from app.repositories.pessoa_repository import PessoaRepository, CoordenadorRepository
from app.models.pessoa import PessoaBase, Coordenador, Estagiario
from typing import Optional

class PessoaService:
    def __init__(self, repository: PessoaRepository):
        self.repository = repository

    async def create_pessoa(self, pessoa: PessoaBase):
        return await self.repository.create_pessoa(pessoa)
    
    async def get_pessoas(self, filtros: Optional[dict] = None):
        return await self.repository.get_pessoas(filtros)
    
    async def update_pessoa(self, pessoa_id: str, pessoa: PessoaBase):
        return await self.repository.update_pessoa(pessoa_id, pessoa)
    
    async def delete_pessoa(self, pessoa_id: str):
        return await self.repository.delete_pessoa(pessoa_id)
    
class CoordenadorService(PessoaService):
    def __init__(self, repository: CoordenadorRepository):
        self.repository = repository

    async def create_coordenador(self, coordenador: Coordenador):
        return await self.repository.create_coordenador(coordenador)
    
    async def get_coordenadores(self, filtros: Optional[dict] = None):
        return await self.repository.get_coordenadores(filtros)
    
    async def update_coordenador(self, coordenador_id: str, coordenador: Coordenador):
        return await self.repository.update_coordenador(coordenador_id, coordenador)
    
    async def delete_coordenador(self, coordenador_id: str):
        return await self.repository.delete_coordenador(coordenador_id)