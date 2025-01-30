from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import Coordenador, PessoaBase
from app.services import CoordenadorService
from app.repositories import PessoaRepository, CoordenadorRepository, MatriculaRepository, EstagiarioRepository
from typing import Optional

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/coordenadores")
async def create_coordenador(coordenador: Coordenador, db = Depends(get_db)):
    coordenador_repository = CoordenadorRepository(db)
    matricula_repository = MatriculaRepository(db, "coordenador_counter")
    pessoa_repository = PessoaRepository(db)
    estagiario_repository = EstagiarioRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)

    existing_pessoa = await pessoa_repository.get_pessoas({"cpf": coordenador.cpf})

    if existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma pessoa com esse CPF"
        )
    
    if not existing_pessoa:
        pessoa = PessoaBase(nome_completo=coordenador.nome_completo, cpf=coordenador.cpf, data_nascimento=coordenador.data_nascimento)
        await pessoa_repository.create_pessoa(pessoa)

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
    pessoa_repository = PessoaRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)
    
    existing_coordenador = await coordenador_repository.get_coordenadores({"_id": ObjectId(coordenador_id)})
    
    if not existing_coordenador or len(existing_coordenador) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coordenador com ID {coordenador_id} não encontrado para atualização"
        )
    
    existing_coordenador = existing_coordenador[0]
    
    if coordenador.cpf != existing_coordenador["cpf"]:
        existing_coordenador_with_same_cpf = await coordenador_repository.get_coordenadores({"cpf": coordenador.cpf})
        if existing_coordenador_with_same_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um Coordenador com esse CPF"
            )
        
    existing_pessoa = await pessoa_repository.get_pessoas({"cpf": coordenador.cpf})
    if existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma pessoa com esse CPF"
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
    pessoa_repository = PessoaRepository(db)
    coordenador_service = CoordenadorService(coordenador_repository, matricula_repository, estagiario_repository)
    
    existing_coordenador = await coordenador_repository.get_coordenadores({"_id": ObjectId(coordenador_id)})

    if existing_coordenador:
        cpf_coordenador = existing_coordenador[0]["cpf"]
        deleted_pessoa_count = await pessoa_repository.delete_pessoa_by_cpf(cpf_coordenador)

        if deleted_pessoa_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhuma pessoa encontrada com o CPF {cpf_coordenador} para exclusão"
            )
        
    deleted_count = await coordenador_service.delete_coordenador(coordenador_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Coordenador com ID {coordenador_id} não encontrado para deleção"
        )
    
    return { "message": "Registro deletado com sucesso!" }