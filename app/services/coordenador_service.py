from app.repositories import CoordenadorRepository, EstagiarioRepository, MatriculaRepository
from app.models import Coordenador
from typing import Optional

class CoordenadorService(CoordenadorRepository):
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