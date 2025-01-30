from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import PessoaBase
from app.services import PessoaService
from app.repositories import PessoaRepository
from typing import Optional

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/pessoas")
async def create_pessoa(pessoa: PessoaBase, db=Depends(get_db)):
    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)

    existing_pessoa = await pessoa_service.get_pessoas({"cpf": pessoa.cpf})
    if existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um registro com esse CPF"
        )
    
    pessoa_id = await pessoa_service.create_pessoa(pessoa)

    return { "message": "Registro Adicionado com Sucesso!", "pessoa_id": pessoa_id }

@router.get("/pessoas")
async def get_pessoas(nome: Optional[str] = None, cpf: Optional[str] = None, data_nascimento: Optional[str] = None, db=Depends(get_db)):
    filtros = {}

    if nome:
        filtros["nome_completo"] = {"$regex": nome, "$options": "i"}
    if cpf:
        filtros["cpf"] = cpf
    if data_nascimento:
        filtros["data_nascimento"] = data_nascimento

    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)
    return await pessoa_service.get_pessoas(filtros)

@router.put("/pessoas/{pessoa_id}")
async def update_pessoa(pessoa_id: str, pessoa: PessoaBase, db=Depends(get_db)):
    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)

    existing_pessoa = await pessoa_repository.get_pessoas({"_id": ObjectId(pessoa_id)})
    
    if not existing_pessoa or len(existing_pessoa) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrado para atualização"
        )
    
    existing_pessoa = existing_pessoa[0]
    
    if pessoa.cpf != existing_pessoa["cpf"]:
        existing_pessoa_with_same_cpf = await pessoa_repository.get_pessoas({"cpf": pessoa.cpf})
        if existing_pessoa_with_same_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma pessoa com esse CPF"
            )
        
    updated_count = await pessoa_service.update_pessoa(pessoa_id, pessoa)

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrada para atualização"
        )
    
    return { "message": "Registro Atualizado com sucesso!" }

@router.delete("/pessoas/{pessoa_id}")
async def delete_pessoa(pessoa_id: str, db=Depends(get_db)):
    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)
    deleted_count = await pessoa_service.delete_pessoa(pessoa_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrada para deleção do registro"
        )
    
    return { "message": "Registro Deletado com sucesso!" }
