from app.repositories import PessoaRepository
from app.models import PessoaBase
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