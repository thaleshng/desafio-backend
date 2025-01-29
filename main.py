from database import app
from app.controllers.pessoa_controller import router as pessoa_router
from app.controllers.coordenador_controller import router as coordenador_router

app.include_router(pessoa_router)
app.include_router(coordenador_router)