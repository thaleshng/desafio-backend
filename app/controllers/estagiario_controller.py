from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models.pessoa import Estagiario
from app.services.pessoa_service import EstagiarioService
from app.repositories.pessoa_repository import EstagiarioRepository, MatriculaRepository
from typing import Optional

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/estagiarios")
async def create_estagiario(estagiario: Estagiario, db = Depends(get_db)):
    estagiario_repository = EstagiarioRepository(db)
    matricula_repository = MatriculaRepository(db, "estagiario_counter")
    estagiario_service = EstagiarioService(estagiario_repository, matricula_repository)

    existing_estagiario = await estagiario_service.get_estagiarios({"cpf": estagiario.cpf})
    if existing_estagiario:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Já existe um Estagiário com esse CPF"
        )
    
    estagiario_id = await estagiario_service.create_estagiario(estagiario)
    return {"message": "Estagiário adicionado com sucesso!", "estagiario_id": estagiario_id}

@router.get("/estagiarios")
async def get_estagiarios(nome: Optional[str] = None, cpf: Optional[str] = None, data_nascimento: Optional[str] = None, matricula: Optional[str] = None, setor: Optional[str] = None, data_entrada: Optional[str] = None, db = Depends(get_db)):
    filtros = {}

    if nome:
        filtros["nome_completo"] = {"$regex": nome, "$options": "i"}
    if cpf:
        filtros["cpf"] = cpf
    if data_nascimento:
        filtros["data_nascimento"] = data_nascimento
    if matricula:
        filtros["matricula"] = matricula
    if setor:
        filtros["setor"] = setor
    if data_entrada:
        filtros["data_entrada"] = data_entrada

    estagiario_repository = EstagiarioRepository(db)
    matricula_repository = MatriculaRepository(db, "estagiario_counter")
    estagiario_service = EstagiarioService(estagiario_repository, matricula_repository)
    return await estagiario_service.get_estagiarios(filtros)

@router.put("/estagiarios/{estagiario_id}")
async def update_estagiario(estagiario_id: str, estagiario: Estagiario, db = Depends(get_db)):
    estagiario_repository = EstagiarioRepository(db)
    matricula_repository = MatriculaRepository(db, "estagiario_counter")
    estagiario_service = EstagiarioService(estagiario_repository, matricula_repository)

    existing_estagiario = await estagiario_repository.get_estagiarios({"_id": ObjectId(estagiario_id)})
    
    if not existing_estagiario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estagiário com ID {estagiario_id} não encontrado para atualização"
        )
    
    existing_estagiario = existing_estagiario[0]

    if estagiario.matricula is None or estagiario.matricula == '':
        estagiario.matricula = existing_estagiario['matricula']

    updated_count = await estagiario_service.update_estagiario(estagiario_id, estagiario)

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estagiário com ID {estagiario_id} não encontrado para atualização"
        )
    
    return { "message": "Registro atualizado com sucesso!" }

@router.delete("/estagiarios/{estagiario_id}")
async def delete_estagiario(estagiario_id: str, db = Depends(get_db)):
    estagiario_repository = EstagiarioRepository(db)
    matricula_repository = MatriculaRepository(db, "estagiario_counter")
    estagiario_service = EstagiarioService(estagiario_repository, matricula_repository)
    deleted_count = await estagiario_service.delete_estagiario(estagiario_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Estagiário com ID {estagiario_id} não encontrado para deleção"
        )
    
    return { "message": "Registro deletado com sucesso!" }