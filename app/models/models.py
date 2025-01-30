import re
from fastapi import HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional
from datetime import datetime

def validar_tipo(values, expected_types):
    for field_name, value in values.items():
        expected_type = expected_types.get(field_name)
        if expected_type and not isinstance(value, expected_type):
            raise HTTPException(
                status_code=422,
                detail=f"O campo '{field_name}' deve ser do tipo {expected_type.__name__}. Recebido: {type(value).__name__}."
            )
    return values

def validar_data(data: str) -> bool:
    if isinstance(data, datetime):
        data = data.strftime('%Y-%m-%d')
    
    if data and not re.match(r'\d{4}-\d{2}-\d{2}', data):
        raise HTTPException(
            status_code=422,
            detail="Data inválida. O formato esperado é YYYY-MM-DD."
        )
    
    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Data inválida. Mês ou dia não correspondem ao calendário."
        )
    return True

class PessoaBase(BaseModel):
    nome_completo: str
    cpf: str
    data_nascimento: datetime

    @field_validator('cpf')
    def validar_cpf(cls, cpf):
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise HTTPException(
                status_code=422,
                detail="CPF inválido. Formato esperado: XXX.XXX.XXX-XX"
            )
        return cpf
    
    @model_validator(mode='before')
    def check_all_required_fields(cls, values):
        for field_name, value in values.items():
            if value is None or value == '':
                raise HTTPException(
                    status_code=422,
                    detail=f"O campo '{field_name}' é obrigatório."
                )
        return values
    
    @model_validator(mode='before')
    def validar_data(cls, values):
        data_nascimento = values.get('data_nascimento')
        if data_nascimento:
            validar_data(data_nascimento)
        return values
    
    @model_validator(mode='before')
    def validar_tipos(cls, values):
        expected_types = {
            "nome_completo": str,
            "cpf": str,
        }
        return validar_tipo(values, expected_types)

class Coordenador(PessoaBase):
    matricula: Optional[str] = None
    setor: str
    estagiarios: List[PessoaBase] = []

    @model_validator(mode='before')
    def validar_tipos(cls, values):
        expected_types = {
            "matricula": str,
            "setor": str,
            "estagiarios": list
        }
        return validar_tipo(values, expected_types)

class Estagiario(PessoaBase):
    matricula: Optional[str] = None
    data_entrada: datetime
    setor: str
    
    @model_validator(mode='before')
    def validar_tipos(cls, values):
        expected_types = {
            "matricula": str,
            "setor": str
        }
        return validar_tipo(values, expected_types)
    
    @model_validator(mode='before')
    def validar_data(cls, values):
        data_entrada = values.get('data_entrada')
        if data_entrada:
            validar_data(data_entrada)
        return values