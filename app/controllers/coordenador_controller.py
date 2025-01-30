from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import Coordenador
from app.services import CoordenadorService
from app.repositories import CoordenadorRepository, MatriculaRepository, EstagiarioRepository
from typing import Optional

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/coordenadores")
async def create_coordenador(coordenador: Coordenador, db = Depends(get_db)):
    coordenador_repository = CoordenadorRepository(db)
    matricula_repository = MatriculaRepository(db, "coordenador_counter")
    estagiario_repository = EstagiarioRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)

    existing_coordenador = await coordenador_service.get_coordenadores({"cpf": coordenador.cpf})
    if existing_coordenador:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Já existe um Coordenador com esse CPF"
        )
    
    existing_estagiario = await estagiario_repository.get_estagiarios({"cpf": coordenador.cpf})
    if existing_estagiario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um Estagiário com esse CPF"
        )
    
    coordenador_id = await coordenador_service.create_coordenador(coordenador)
    return {"message": "Coordenador adicionado com sucesso!", "coordenador_id": coordenador_id}

@router.get("/coordenadores")
async def get_coordenadores(nome: Optional[str] = None, cpf: Optional[str] = None, data_nascimento: Optional[str] = None, matricula: Optional[str] = None, setor: Optional[str] = None, db = Depends(get_db)):
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

    coordenador_repository = CoordenadorRepository(db)
    matricula_repository = MatriculaRepository(db, "coordenador_counter")
    estagiario_repository = EstagiarioRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)
    coordenadores = await coordenador_service.get_coordenadores(filtros)

    for coordenador in coordenadores:
        estagiarios = await estagiario_repository.get_estagiarios({"setor": coordenador["setor"]})
        coordenador["estagiarios"] = estagiarios
    return coordenadores

@router.put("/coordenadores/{coordenador_id}")
async def update_coordenadores(coordenador_id: str, coordenador: Coordenador, db = Depends(get_db)):
    coordenador_repository = CoordenadorRepository(db)
    matricula_repository = MatriculaRepository(db, "coordenador_counter")
    estagiario_repository = EstagiarioRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)
    existing_coordenador = await coordenador_repository.get_coordenadores({"_id": ObjectId(coordenador_id)})
    
    if not existing_coordenador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coordenador com ID {coordenador_id} não encontrado para atualização"
        )
    
    if coordenador.cpf != existing_coordenador[0]["cpf"]:
        existing_coordenador_with_same_cpf = await coordenador_repository.get_coordenadores({"cpf": coordenador.cpf})
        if existing_coordenador_with_same_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um Coordenador com esse CPF"
            )
        
    existing_estagiario = await estagiario_repository.get_estagiarios({"cpf": coordenador.cpf})
    if existing_estagiario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um Estagiário com esse CPF"
        )

    if coordenador.matricula is None or coordenador.matricula == '':
        coordenador.matricula = existing_coordenador['matricula']

    updated_count = await coordenador_service.update_coordenador(coordenador_id, coordenador)

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coordenador com ID {coordenador_id} não encontrado para atualização"
        )
    
    return { "message": "Registro atualizado com sucesso!" }

@router.delete("/coordenadores/{coordenador_id}")
async def delete_coordenador(coordenador_id: str, db = Depends(get_db)):
    coordenador_repository = CoordenadorRepository(db)
    matricula_repository = MatriculaRepository(db, "coordenador_counter")
    estagiario_repository = EstagiarioRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)
    deleted_count = await coordenador_service.delete_coordenador(coordenador_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coordenador com ID {coordenador_id} não encontrado para deleção"
        )
    
    return { "message": "Registro deletado com sucesso!" }