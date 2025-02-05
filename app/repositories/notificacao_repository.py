from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import NotificacaoBase
from typing import List

class NotificacaoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db["notificacoes"]

    async def create_notificacao(self, notificação: NotificacaoBase) -> str:
        result = await self.db.insert_one(notificação.model_dump())
        return str(result.inserted_id)
    
    async def get_notificacoes(self) -> List[dict]:
        notificacoes = []
        async for notificacao in self.db.find():
            notificacao["_id"] = str(notificacao["_id"])
            notificacoes.append(notificacao)
        return notificacoes