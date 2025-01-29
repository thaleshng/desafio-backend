from app.repositories.pessoa_repository import PessoaRepository, CoordenadorRepository, EstagiarioRepository, MatriculaRepository
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
    def __init__(self, repository: CoordenadorRepository, matricula_repository: MatriculaRepository, estagiario_repository: EstagiarioRepository):
        self.repository = repository
        self.matricula_repository = matricula_repository
        self.estagiario_repository = estagiario_repository

    async def create_coordenador(self, coordenador: Coordenador):
        return await self.repository.create_coordenador(coordenador)
    
    async def get_coordenadores(self, filtros: Optional[dict] = None):
        return await self.repository.get_coordenadores(filtros)
    
    async def update_coordenador(self, coordenador_id: str, coordenador: Coordenador):
        return await self.repository.update_coordenador(coordenador_id, coordenador)
    
    async def delete_coordenador(self, coordenador_id: str):
        return await self.repository.delete_coordenador(coordenador_id)
    
class EstagiarioService(EstagiarioRepository):
    def __init__(self, repository: EstagiarioRepository, matricula_repository: MatriculaRepository, coordenador_repository: CoordenadorRepository):
        self.repository = repository
        self.matricula_repository = matricula_repository
        self.coordenador_repository = coordenador_repository

    async def create_estagiario(self, estagiario: Estagiario):
        return await self.repository.create_estagiario(estagiario)
    
    async def get_estagiarios(self, filtros: Optional[dict] = None):
        return await self.repository.get_estagiarios(filtros)
    
    async def update_estagiario(self, estagiario_id: str, estagiario: Estagiario):
        return await self.repository.update_estagiario(estagiario_id, estagiario)
    
    async def delete_estagiario(self, estagiario_id: str):
        return await self.repository.delete_estagiario(estagiario_id)