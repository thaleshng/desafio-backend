from database import app
from app.controllers.pessoa_controller import router as pessoa_router
from app.controllers.coordenador_controller import router as coordenador_router
from app.controllers.estagiario_controller import router as estagiario_router
from app.controllers.notificacao_controller import router as notificacao_router

app.include_router(pessoa_router)
app.include_router(coordenador_router)
app.include_router(estagiario_router)
app.include_router(notificacao_router)