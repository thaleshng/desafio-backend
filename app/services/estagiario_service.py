from app.repositories import CoordenadorRepository, EstagiarioRepository, MatriculaRepository
from app.models import Estagiario
from typing import Optional


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
        estagiario_dict = estagiario.model_dump()
        return await self.repository.update_estagiario(estagiario_id, estagiario_dict)
    
    async def delete_estagiario(self, estagiario_id: str):
        return await self.repository.delete_estagiario(estagiario_id)