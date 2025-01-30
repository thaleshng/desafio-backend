from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import PessoaBase
from app.services import PessoaService
from app.repositories import PessoaRepository, CoordenadorRepository, EstagiarioRepository
from typing import Optional

router = APIRouter()

def get_db(request: Request):
    return request.app.mongodb_db

@router.post("/pessoas", tags=["pessoas"])
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

@router.get("/pessoas", tags=["pessoas"])
async def get_pessoas(nome: Optional[str] = None, cpf: Optional[str] = None, db=Depends(get_db)):
    filtros = {}

    if nome:
        filtros["nome_completo"] = {"$regex": nome, "$options": "i"}
    if cpf:
        filtros["cpf"] = cpf

    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)
    return await pessoa_service.get_pessoas(filtros)

@router.put("/pessoas/{pessoa_id}", tags=["pessoas"])
async def update_pessoa(pessoa_id: str, pessoa: PessoaBase, db=Depends(get_db)):
    pessoa_repository = PessoaRepository(db)
    pessoa_service = PessoaService(pessoa_repository)
    
    existing_pessoa = await pessoa_repository.get_pessoas({"_id": ObjectId(pessoa_id)})

    if not existing_pessoa or len(existing_pessoa) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrada para atualização"
        )

    existing_pessoa = existing_pessoa[0]

    # Verificação de duplicidade de CPF
    if pessoa.cpf != existing_pessoa["cpf"]:
        # Verifica se o novo CPF já existe em outra pessoa
        pessoa_com_novo_cpf = await pessoa_repository.get_pessoas({
            "cpf": pessoa.cpf,
            "_id": {"$ne": ObjectId(pessoa_id)}  # Exclui o próprio registro
        })
        
        if pessoa_com_novo_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe outra pessoa com este CPF"
            )

    pessoa_data = PessoaBase(
        nome_completo=pessoa.nome_completo,
        cpf=pessoa.cpf,
        data_nascimento=pessoa.data_nascimento
    )

    if pessoa.cpf != existing_pessoa["cpf"]:
        update_pessoa_count = await pessoa_repository.update_pessoa_by_cpf(existing_pessoa["cpf"], pessoa_data)
        if update_pessoa_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nenhuma pessoa encontrada com o CPF {existing_pessoa['cpf']} para atualização"
            )

        coordenador_repository = CoordenadorRepository(db)
        estagiario_repository = EstagiarioRepository(db)

        await coordenador_repository.update_coordenador_by_cpf(existing_pessoa["cpf"], pessoa.cpf)
        await estagiario_repository.update_estagiario_by_cpf(existing_pessoa["cpf"], pessoa.cpf)

    coordenador_repository = CoordenadorRepository(db)
    estagiario_repository = EstagiarioRepository(db)

    await coordenador_repository.update_coordenador_fields_by_cpf(pessoa.cpf, {
        "nome_completo": pessoa.nome_completo,
        "data_nascimento": pessoa.data_nascimento
    })

    await estagiario_repository.update_estagiario_fields_by_cpf(pessoa.cpf, {
        "nome_completo": pessoa.nome_completo,
        "data_nascimento": pessoa.data_nascimento
    })

    await pessoa_service.update_pessoa(pessoa_id, pessoa) 

    return { "message": "Registro atualizado com sucesso!" }


@router.delete("/pessoas/{pessoa_id}", tags=["pessoas"])
async def delete_pessoa(pessoa_id: str, db=Depends(get_db)):
    pessoa_repository = PessoaRepository(db)
    coordenador_repository = CoordenadorRepository(db)
    estagiario_repository = EstagiarioRepository(db)
    pessoa_service = PessoaService(pessoa_repository)

    existing_pessoa = await pessoa_repository.get_pessoas({"_id": ObjectId(pessoa_id)})

    if not existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrada para deleção"
        )

    cpf_pessoa = existing_pessoa[0]["cpf"]

    deleted_count = await pessoa_service.delete_pessoa(pessoa_id)

    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com ID {pessoa_id} não encontrada para deleção do registro"
        )

    deleted_coordenador_count = await coordenador_repository.delete_coordenador_by_cpf(cpf_pessoa)

    deleted_estagiario_count = await estagiario_repository.delete_estagiario_by_cpf(cpf_pessoa)

    return { 
        "message": "Registro Deletado com sucesso!", 
        "deleted_coordenador_count": deleted_coordenador_count, 
        "deleted_estagiario_count": deleted_estagiario_count 
    }
