from app.repositories import NotificacaoRepository
from app.models import NotificacaoBase
from typing import List

class NotificacaoService:
    def __init__(self, repository: NotificacaoRepository):
        self.repository = repository

    async def create_notificacao(self, notificacao: NotificacaoBase) -> str:
        return await self.repository.create_notificacao(notificacao)
    
    async def get_notificacoes(self) -> List[dict]:
        return await self.repository.get_notificacoes()