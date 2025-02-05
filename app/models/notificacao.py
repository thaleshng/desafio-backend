from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class NotificacaoBase(BaseModel):
    dataHora: datetime = Field(default_factory=datetime.now)
    tipo: str
    conteudo: str
    destinatarios: List[str]