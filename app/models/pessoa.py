import re
from fastapi import HTTPException
from pydantic import BaseModel, field_validator, model_validator
from typing import List
from datetime import date, datetime

class PessoaBase(BaseModel):
    nome_completo: str
    cpf: str
    data_nascimento: datetime

    @model_validator(mode='before')
    def validar_cpf(cls, values):
        cpf = values.get('cpf')
        if cpf and not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            raise HTTPException(
                status_code=422,
                detail="CPF inválido. O formato esperado é XXX.XXX.XXX-XX."
            )
        return values
    
    @model_validator(mode='before')
    def check_all_required_fields(cls, values):
        for field_name, value in values.items():
            if value is None or value == '':
                raise HTTPException(
                    status_code=422,
                    detail=f"O campo '{field_name}' é obrigatório."
                )
        return values
    
    def dict(self, *args, **kwargs):
        data_dict = super().dict(*args, **kwargs)
        if 'data_nascimento' in data_dict:
            data_dict['data_nascimento'] = data_dict['data_nascimento'].date().isoformat()  # Retorna como string no formato 'YYYY-MM-DD'
        return data_dict

class Coordenador(PessoaBase):
    matricula: str
    setor: str
    estagiarios: List[PessoaBase] = []

class Estagiario(PessoaBase):
    matricula: str
    data_entrada: str
    setor: str