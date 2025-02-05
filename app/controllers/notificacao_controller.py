from fastapi import APIRouter, Depends, HTTPException, Request
from app.models import NotificacaoBase
from app.services import NotificacaoService
from app.repositories import NotificacaoRepository
from typing import List

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/notificacoes", tags=["notificacoes"])
async def create_notificacao(notificacao: NotificacaoBase, db = Depends(get_db)):
    notificacao_repository = NotificacaoRepository(db)
    notificacao_service = NotificacaoService(notificacao_repository)

    notificacao_id = await notificacao_service.create_notificacao(notificacao)

    return {"message": "Notificação registrada!", "notificacao_id": notificacao_id}

@router.get("/notificacoes", tags=["notificacoes"])
async def get_notificacoes(db = Depends(get_db)):
    notificacao_repository = NotificacaoRepository(db)
    notificacao_service = NotificacaoService(notificacao_repository)
    return await notificacao_service.get_notificacoes()